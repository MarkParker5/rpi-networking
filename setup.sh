# install dependencies

sudo apt update
sudo apt upgrade -y
sudo apt install dnsmasq hostapd dhcpd -y

# give user permission to edit files so python doesn't have to be run as root (sudo)

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
