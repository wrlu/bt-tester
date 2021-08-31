import bluetooth

def bt_discover():
    nearby_devices = bluetooth.discover_devices(lookup_names=True)
    for nearby_device in nearby_devices:
        print(nearby_device)
    return nearby_devices
