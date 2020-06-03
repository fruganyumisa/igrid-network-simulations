def spawnStations(stations=0, smart_meters=0, actuator=0, mac_prefix="00:00:00:00:00"):
    """

    """
    # ip = "10.0.0.1/8"
    # position = "10,20,0"
    # antenna_height = "1"
    # antenna_gain = "5"
    # active_scan = 1
    # scan_freq = "2412 2437 2462"
     
    #  generate smart meters 
    generate(device_control=0, device_total=smart_meters, prefix_name="smeter", mac_prefix=mac_prefix)

    # generate actuator
    generate(device_control=smart_meters, device_total=actuator, prefix_name="actuator", mac_prefix=mac_prefix)

    # generate stations
    generate(device_control=smart_meters + actuator, device_total=stations, prefix_name="sta", mac_prefix=mac_prefix)


def generate(device_control, device_total, prefix_name, mac_prefix):
    for i in range(device_total):
        device_control += 1
        device_name = f'{prefix_name}{i + 1}'
        mac_addr = f'{mac_prefix}:{"{:0>2d}".format(device_control)}'

        print("Device: ", device_name, "mac_addr:", mac_addr)

if __name__ == "__main__":
    spawnStations(stations=10, smart_meters=3, actuator=5)