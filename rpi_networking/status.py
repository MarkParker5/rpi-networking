from .tools import call_subprocess


def is_wlan_connected() -> bool:
    return call_subprocess("iwgetid")

def is_eth_connected() -> bool:
    return call_subprocess("ifconfig eth0")

def is_wlan_global_connected() -> bool:
    return call_subprocess("ping -I wlan0 -c 1 google.com")

def is_eth_global_connected() -> bool:
    return call_subprocess("ping -I eth0 -c 1 google.com")

def is_wps_running() -> bool:
    return (
        call_subprocess(
            'wpa_cli -i wlan0 wps_status | grep -o "WPS-STATE=[a-zA-Z]*" | cut -d"=" -f2'
        )
        == "running"
    )
