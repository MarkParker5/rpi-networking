import time

from configuration import hosts_content, hosts_path
from tools import call_subprocess


def set_hostname(hostname: str):
    call_subprocess(f"sudo hostnamectl set-hostname {hostname}")

    with open(hosts_path, "w") as f:
        f.write(hosts_content)
        f.write(f"127.0.1.1 {hostname} {hostname}.localdomain {hostname}.local\n")

    return hostname

def restart_interfaces():  # apply new hostname without reboot
    call_subprocess("sudo ifdown wlan0")
    call_subprocess("sudo ifdown eth0")
    call_subprocess("sudo ifdown ap0")
    time.sleep(1)
    call_subprocess("sudo ifup wlan0")
    call_subprocess("sudo ifup eth0")
    call_subprocess("sudo ifdown ap0")
