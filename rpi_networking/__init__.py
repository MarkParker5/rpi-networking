import configuration
import hostname
import hotspot
import status
import wifi


def start_hotspot_if_needed():
    connected = status.is_wlan_connected()
    if not connected and not hotspot.is_hotspot_running:
        hotspot.start_hotspot()
    elif connected and hotspot.is_hotspot_running:
        hotspot.stop_hotspot()
