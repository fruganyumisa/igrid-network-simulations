def spawnStations(net, stations=0, smart_meters=0, actuator=0, mac_prefix="00:00:00:00:00", ip_prefix="10.0.0", cidr="/1"):
    """
    spawnStations generate specified number of IoT devices (stations) and assign to them (stations) 
    specific mac address and ip address based on mac_prefic and ip_prefix

    mac_prefix defines first 5 octet number(s) in mac address. The last octect will be generated from device index.

    ip_prefix  defines the network address. The host address will be generated from device index.
    """

    #  generate smart meters
    net = generate(net, device_control=0, device_total=smart_meters,
                   prefix_name="smeter", mac_prefix=mac_prefix, ip_prefix=ip_prefix, cidr=cidr)

    # generate actuator
    net = generate(net, device_control=smart_meters, device_total=actuator,
                   prefix_name="actuator", mac_prefix=mac_prefix, ip_prefix=ip_prefix, cidr=cidr)

    # generate stations
    net = generate(net, device_control=smart_meters + actuator,
                   device_total=stations, prefix_name="sta", mac_prefix=mac_prefix, ip_prefix=ip_prefix, cidr=cidr)

    return net


def generate(net, device_control, device_total, prefix_name, mac_prefix, ip_prefix, cidr):
    """
    generate creates station and add it to mininet.net object which contain all spawned network devices.
    """
    for i in range(device_total):
        device_control += 1
        device_name = f'{prefix_name}{i + 1}'
        mac_addr = f'{mac_prefix}:{"{:0>2d}".format(device_control)}'
        ip_addr = f'{ip_prefix}.{device_control}{cidr}'
        pos = f'{device_control},{device_control},0'

        print("Device: ", device_name, "mac_addr:",
              mac_addr, "ip_addr:", ip_addr, "position:", pos)
        net.addStation(device_name, mac=mac_addr, ip=ip_addr,
                       antennaHeight='1', antennaGain='5',  position=pos, active_scan=1, scan_freq="2412 2437 2462")
    return net


def spawnAccessPoint(net, access_point=0):
    for i in range(access_point):
        ap_name = f'ap{i + 1}'
        ssid = f'iGrid-{ap_name}'
        curr = i + 1
        pos = f'{10 * curr},{30 * curr},0'

        print("ap_name:", ap_name, "ssid:", ssid, "pos:", pos)
        net.addAccessPoint(ap_name, ssid=ssid, mode='g', channel='6',
                           model='DI524', position=pos, range='100')
    return net
