import math
from random import random
from mininet.node import Controller
from mn_wifi.net import Mininet_wifi
from mn_wifi.link import wmediumd
from mn_wifi.node import OVSKernelAP
from mininet.log import setLogLevel, info
from mn_wifi.cli import CLI as mininet_cli


class IGRID:
    net = Mininet_wifi(controller=Controller, link=wmediumd,
                       accessPoint=OVSKernelAP, noise_th=-91,  ac_method='sf')

    def __init__(self, sensors=0, smart_meters=0, actuators=0):
        self.sensors = []
        self.smart_meters = []
        self.actuators = []
        self.access_points = []

        self.__addAccessPoints__()

        server = self.net.addHost(
            'server', mac='00:00:00:00:08:00', ip='10.10.10.254/8')

        self.switch = self.net.addSwitch('sw',  dpid=self.__int2dpid__(1))

        self.controller = self.net.addController('cl', controller=Controller)

        self.net.setPropagationModel(model="logDistance", exp=4)

        info("*** Configuring wifi nodes\n")
        self.net.configureWifiNodes()
        self.net.plotGraph(max_x=200, max_y=200)

        info("*** Enabling Association control (AP)\n")
        self.net.auto_association()

        info("*** Creating links and associations\n")
        self.net.addLink(self.switch, server)
        for ap in self.access_points:
            self.net.addLink(ap, self.switch)



    def start(self):
        self.net.build()
        self.controller.start()
        self.switch.start([self.controller])
        
        for ap in self.access_points:
            ap.start([self.controller])

        mininet_cli(self.net)

    def stop(self):
        self.net.stop()

    def __int2dpid__(self, dpid):
        try:
            dpid = hex(dpid)[2:]
            dpid = '0' * (16 - len(dpid)) + dpid
            return dpid
        except IndexError:
            raise Exception('Unable to derive default datapath ID - '
                            'please either specify a dpid or use a '
                            'canonical switch name such as s23.')

    def __generate__(self, net, device_control, device_total, prefix_name, mac_prefix, ip_prefix, cidr, coordinate):
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
            self.net.addStation(device_name, mac=mac_addr, ip=ip_addr,
                                antennaHeight='1', antennaGain='5',  position=pos)
            # , active_scan=1, scan_freq="2412 2437 2462"
        return net

    def __addAccessPoints__(self):
        ap1 = self.net.addAccessPoint(
            'ap1', ssid='iGrid-ap1', mode='g', channel='6', model='DI524', position='50,125,0', range='100')
        self.access_points.append(ap1)

        ap2 = self.net.addAccessPoint(
            'ap2', ssid='iGrid-ap2', mode='g', channel='1', model='DI524', position='100,75,0', range='100')
        self.access_points.append(ap2)

        ap3 = self.net.addAccessPoint('ap3', ssid='iGrid-ap3', mode='g',
                                      channel='3', model='DI524', position='125,125,0', range='100')
        self.access_points.append(ap3)

    def __generateStationsCoordinates__(self, radius, reference=(0, 0)):
        """
            generates a random station x, y coordinate which lies within the AP coverage radius
            and returns its X and Y coordinates as a tuple.
        """
        coordinates = []

        total_nodes = len(self.sensors) + \
            len(self.smart_meters) + len(self.actuators)
        for _ in range(0, total_nodes):
            r = radius * math.sqrt(random())
            theta = 2 * math.pi * random()
            coordinates.append((round(
                reference[0] + r * math.cos(theta)), round(reference[1] + r * math.sin(theta))))
        return coordinates
