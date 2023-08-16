from .tools import call_subprocess


is_hotspot_running: bool = False

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
        global is_hotspot_running
        is_hotspot_running = True
        return True
    else:
        return False

def stop_hotspot() -> bool:
    if call_subprocess("sudo service hostapd stop"):
        global is_hotspot_running
        is_hotspot_running = False
        return True
    else:
        return False
