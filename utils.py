import math
from random import random


def spawnStations(net, sensors=0, smart_meters=0, actuator=0, mac_prefix="00:00:00:00:00", ip_prefix="10.0.0", cidr="/8"):
    """
    spawnStations generate specified number of IoT devices (sensors) and assign to them (stations) 
    specific mac address and ip address based on mac_prefic and ip_prefix

    mac_prefix defines first 5 octet number(s) in mac address. The last octect will be generated from device index.

    ip_prefix  defines the network address. The host address will be generated from device index.
    """

    # stations coordinates
    coordinate = generateStationsCoordinates(radius=100, reference=(
        100, 100), count=sensors + smart_meters + actuator)

    #  generate smart meters
    net = generate(net, device_control=0, device_total=smart_meters, prefix_name="smeter",
                   mac_prefix=mac_prefix, ip_prefix=ip_prefix, cidr=cidr, coordinate=coordinate[:smart_meters])

    # generate actuator
    net = generate(net, device_control=smart_meters, device_total=actuator, prefix_name="actuator", mac_prefix=mac_prefix,
                   ip_prefix=ip_prefix, cidr=cidr, coordinate=coordinate[smart_meters:smart_meters + actuator])

    # generate sensors
    net = generate(net, device_control=smart_meters + actuator, device_total=sensors, prefix_name="sensor",
                   mac_prefix=mac_prefix, ip_prefix=ip_prefix, cidr=cidr, coordinate=coordinate[smart_meters+actuator:])

    return net


def generate(net, device_control, device_total, prefix_name, mac_prefix, ip_prefix, cidr, coordinate):
    """
    generate creates station and add it to mininet.net object which contain all spawned network devices.
    """
    for i in range(device_total):
        device_control += 1
        device_name = '{}{}'.format(prefix_name, i + 1)
        mac_addr = '{}:{:0>2d}'.format(mac_prefix, device_control)
        ip_addr = '{}.{}{}'.format(ip_prefix, device_control, cidr)
        pos = '{},{},0'.format(coordinate[i][0], coordinate[i][1])

        print("Device: ", device_name, "mac_addr:",
              mac_addr, "ip_addr:", ip_addr, "position:", pos)
        net.addStation(device_name, mac=mac_addr, ip=ip_addr,
                       antennaHeight='1', antennaGain='5',  position=pos)
        # , active_scan=1, scan_freq="2412 2437 2462"
    return net


def spawnAccessPoint(net, access_point=0):
    for i in range(access_point):
        ap_name = 'ap{}'.format(i + 1)
        ssid = 'iGrid-{}'.format(ap_name)
        curr = i + 1

        print("ap_name:", ap_name, "ssid:", ssid, "pos:", "100,100,0")
        net.addAccessPoint(ap_name, ssid=ssid, mode='g', channel='6',
                           model='DI524', position="100,100,0", range='100')
    return net


def generateStationsCoordinates(radius, reference=(0, 0), count=0):
    """
    Function generates a random station x, y coordinate which lies within the AP coverage radius
    and returns its X and Y coordinates as a tuple.
    """
    coordinates = []
    for i in range(0, count):
        r = radius * math.sqrt(random())
        theta = 2 * math.pi * random()
        coordinates.append(
            (reference[0] + r * math.cos(theta), reference[1] + r * math.sin(theta)))
    return coordinates
