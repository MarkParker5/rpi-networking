import re
from dataclasses import dataclass
from subprocess import CalledProcessError
from typing import Generator

from .configuration import (
    interfaces_path,
    network_interfaces_content,
    wpa_supplicant_content,
    wpa_supplicant_path,
)
from .tools import call_subprocess, check_subprocess_output


# Variables

country: str = 'GB'

# String parsing

network_regex = re.compile(
    r'network=\{\s+ssid="(?P<ssid>.*)"\s+psk="(?P<psk>.*)"\s+id_str="(?P<id_str>.*)"\s+\}'
)

cell_regex = re.compile(
    r'Cell(?:.|\n)*?Frequency:(?P<frequency>.+)(?:.|\n)*?Quality=(?P<quality>.+)(?:.|\n)*?Encryption key:(?P<encrypted>.+)(?:.|\n)*?ESSID:"(?P<ssid>.+)"'
)

network_record = (
    lambda network, i: f"""
network={{
        ssid="{network.ssid}"
        psk="{network.psk}"
        id_str="AP{i}"
}}
"""
)

# Models

class InterfaceBusyException(Exception):
    pass

@dataclass
class Cell:
    ssid: str
    quality: float
    frequency: str
    encrypted: bool
    # encryption_type: str

@dataclass
class Network:
    ssid: str
    psk: str
    id_str: str = ""

# Functions

def read_networks() -> list[Network]:
    networks: list[Network] = []
    with open(wpa_supplicant_path, "r") as f:
        for match in network_regex.finditer(f.read()):
            networks.append(Network(**match.groupdict()))
    return networks

def write_networks(networks: list[Network]):
    with open(wpa_supplicant_path, "w") as f:
        f.write(wpa_supplicant_content(country))

        for i, network in enumerate(networks):
            f.write(network_record(network, i))

    with open(interfaces_path, "w") as f:
        f.write(network_interfaces_content)

        for i in range(len(networks)):
            f.write(f"iface AP{i} inet dhcp")

def add_network(ssid: str, psk: str):
    networks = read_networks()
    networks.append(Network(ssid, psk))
    write_networks(networks)

def reconnect() -> bool:
    return call_subprocess("sudo wpa_cli -i wlan0 reconfigure")

def scan() -> Generator[Cell, None, None]:
    try:
        output = check_subprocess_output("sudo iwlist wlan0 scan")
    except CalledProcessError as exc:
        raise InterfaceBusyException from exc

    for match in cell_regex.finditer(output):
        groups = match.groupdict()

        quality, max = map(float, groups["quality"].split(" ")[0].split("/"))

        ssid = groups["ssid"].strip()
        quality = round(quality / max, 2)
        frequency = re.sub(r"\(Channel.*\)", "", groups["frequency"]).strip()
        encrypted = groups["encrypted"] == "on"

        yield Cell(ssid, quality, frequency, encrypted)

def start_wps() -> bool:
    return call_subprocess("wpa_cli -i wlan0 wps_pbc")
