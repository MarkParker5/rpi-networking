#!/bin/bash

sudo apt update
# sudo apt upgrade -y
sudo apt install dnsmasq hostapd dhcpd -y

# give user permission to edit files so python doesn't have to be run as root (sudo)

files=(
  "/etc/dnsmasq.conf"
  "/etc/hosts"
  "/etc/default/hostapd"
  "/etc/hostapd/hostapd.conf"
  "/etc/network/interfaces"
  "/etc/network/interfaces.d"
  "/etc/wpa_supplicant/wpa_supplicant.conf"
)

touch /etc/hostapd/hostapd.conf

for file in "${files[@]}"; do
  sudo chown "$USER" "$file"
  sudo chmod 644 "$file"
done;
