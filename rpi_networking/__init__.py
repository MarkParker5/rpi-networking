from . import configuration
from . import hostname
from . import hotspot
from . import status
from . import wifi


def start_hotspot_if_needed():
    connected = status.is_wlan_connected()
    hotspot_up = hotspot.is_hotspot_up()
    
    if not connected and not hotspot_up:
        hotspot.start_hotspot()
    elif connected and hotspot_up:
        hotspot.stop_hotspot()
