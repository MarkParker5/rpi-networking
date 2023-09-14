interfaces_path = r"/etc/network/interfaces"
default_hostapd_path = r"/etc/default/hostapd"
hostapd_conf_path = r"/etc/hostapd/hostapd.conf"
dnsmaq_conf_path = r"/etc/dnsmasq.conf"
wpa_supplicant_path = r"/etc/wpa_supplicant/wpa_supplicant.conf"
hosts_path = r"/etc/hosts"

network_interfaces_content = """source-directory /etc/network/interfaces.d

auto lo
auto eth0
auto wlan0
auto ap0

iface eth0 inet dhcp
iface lo inet loopback

allow-hotplug ap0
iface ap0 inet static
    address 192.168.10.1
    netmask 255.255.255.0
    hostapd /etc/hostapd/hostapd.conf

allow-hotplug wlan0
iface wlan0 inet manual
    wpa-roam /etc/wpa_supplicant/wpa_supplicant.conf

"""

default_hostapd_content = """DAEMON_CONF="/etc/hostapd/hostapd.conf"
"""

hostapd_conf_content = """ctrl_interface=/var/run/hostapd
ctrl_interface_group=0
interface=ap0
driver=nl80211
ssid=MajorDom Hub
hw_mode=g
channel=11
wmm_enabled=0
macaddr_acl=0
auth_algs=1
wpa=2
wpa_passphrase=majordom
wpa_key_mgmt=WPA-PSK
wpa_pairwise=TKIP CCMP
rsn_pairwise=CCMP
"""

dnsmasq_conf_content = """interface=lo,ap0
no-dhcp-interface=lo,wlan0
bind-interfaces
server=8.8.8.8
#domain-needed
#bogus-priv
dhcp-range=192.168.10.50,192.168.10.150,12h
address=/majordom-hub/192.168.10.1
"""

wpa_supplicant_content = (
    lambda country: f"""country={country}
ctrl_interface=DIR=/var/run/wpa_supplicant GROUP=netdev
ap_scan=1
update_config=1
"""
)

hosts_content = """
127.0.0.1\tlocalhost
::1\tlocalhost ip6-localhost ip6-loopback
ff02::1\tip6-allnodes
ff02::2\tip6-allrouters
"""

def write(file: str, content: str):
    with open(file, "w") as f:
        f.write(content)

def write_interfaces():
    write(interfaces_path, network_interfaces_content)

def write_default_hostapd():
    write(default_hostapd_path, default_hostapd_content)

def write_hostapd_conf():
    write(hostapd_conf_path, hostapd_conf_content)

def write_dnsmasq_conf():
    write(dnsmaq_conf_path, dnsmasq_conf_content)

def write_wpa_supplicant(country: str = "GB"):
    write(wpa_supplicant_path, wpa_supplicant_content(country))

def write_hosts():
    write(hosts_path, hosts_content)

def write_all():
    write_interfaces()
    write_default_hostapd()
    write_hostapd_conf()
    write_dnsmasq_conf()
    write_wpa_supplicant()
    write_hosts()
