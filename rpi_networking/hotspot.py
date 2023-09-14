from .tools import call_subprocess


def is_hotspot_up() -> bool:
    return call_subprocess('ip link show ap0 | grep "state UP"')

def start_hotspot() -> bool:
    commands = [
        "sudo service hostapd stop",
        "sudo service dnsmasq stop",
        "sudo service dhcpcd stop",
        "sudo iw dev wlan0 interface add ap0 type __ap",
        "sudo service hostapd start",
        "sudo service dnsmasq start",
        "sudo service dhcpcd start",
    ]

    if call_subprocess(" && ".join(commands)):
        return is_hotspot_up()
    else:
        return False

def stop_hotspot() -> bool:
    if call_subprocess("sudo service hostapd stop"):
        return not is_hotspot_up()
    else:
        return False
