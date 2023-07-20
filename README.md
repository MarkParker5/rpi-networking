# rpi-networking
Control wifi, hotspot and hostname of Raspberry Pi

## Requirments 

Python3.10+

## Installation

### Using pip:

```sh
pip3 install rpi-networking 
```

### Using poetry

```sh
poetry add rpi-networking
```

## Prepare system

### Automatically 

Via curl

```sh
sh -c "$(curl -fsSL https://raw.githubusercontent.com/MarkParker5/rpi-networking/master/setup.sh)"
```

Or via wget

```sh
sh -c "$(wget https://raw.githubusercontent.com/MarkParker5/rpi-networking/master/setup.sh -O -)"
```

### Manually

#### Dependencies

```sh
sudo apt update ; \
sudo apt upgrade -y ; \
sudo apt install dnsmasq hostapd dhcpd -y
```

#### Give permissions to edit configuration files (optional)

Give user permission to edit configuration files so python doesn't have to be run as root (sudo)

```sh
files=(
  "/boot/config.txt"
  "/etc/dnsmasq.conf"
  "/etc/hosts"
  "/etc/default/hostapd"
  "/etc/hostapd/hostapd.conf"
  "/etc/network/interfaces"
  "/etc/network/interfaces.d"
  "/etc/wpa_supplicant/wpa_supplicant.conf"
)

for file in "${files[@]}"; do
  sudo chown "$USER" "$file"
  sudo chmod 644 "$file"
done;
```

## Docs

### Configuration

There are functions for initial configuration setup.

```python
# rpi-networking.configuraion

def write_interfaces():

def write_default_hostapd():

def write_hostapd_conf():

def write_dnsmasq_conf():

def write_wpa_supplicant(country: str = "GB"):

def write_hosts():

def enable_spi():

def write_all(): # calls all functions above
```

**In most cases you only need to call `write_all()` once to setup all configuration files.**

### Hostname

```python
# rpi-networking.hostname

def set_hostname(hostname: str):
    
def restart_interfaces():  # apply new hostname without reboot
```

### Hotspot

```python
# rpi-networking.hotspot

is_hotspot_running: bool

def start_hotspot() -> bool:
    
def stop_hotspot() -> bool:
```

The `bool` return value is `True` if function finished without errors (exit code 0), else `False`

### Status

```python
# rpi-networking.status

def is_wlan_connected() -> bool:

def is_eth_connected() -> bool:

def is_wlan_global_connected() -> bool: # 'global' means internet access

def is_eth_global_connected() -> bool:

def is_wps_running() -> bool:
```

### WiFi

```python
# rpi-networking.wifi

class InterfaceBusyException(Exception): 
    pass

class Cell:
    ssid: str
    quality: float
    frequency: str
    encrypted: bool

class Network:
    ssid: str
    psk: str
    id_str: str

# Functions

def read_networks() -> list[Network]:

def write_networks(networks: list[Network]):

def add_network(ssid: str, psk: str):

def reconnect() -> bool: # connect to the best available network

def scan() -> Generator[Cell, None, None]:

def start_wps() -> bool:
```
