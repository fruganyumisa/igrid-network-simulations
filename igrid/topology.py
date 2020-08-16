import math
from random import random, randint
from netaddr import IPNetwork
from mininet.node import Controller
from mn_wifi.net import Mininet_wifi
from mn_wifi.link import wmediumd
from mn_wifi.node import OVSKernelAP
from mininet.log import setLogLevel, info
from mn_wifi.cli import CLI as mininet_cli


class IGRID(object):
    net = Mininet_wifi(controller=Controller, link=wmediumd,
                       accessPoint=OVSKernelAP, noise_th=-91,  ac_method='sf')

    def __init__(self, sensors=0, smart_meters=0, actuators=0, max_x=200, max_y=200):
        self.sensors = sensors
        self.smart_meters = smart_meters
        self.actuators = actuators
        self.max_x = max_x
        self.max_y = max_y

        self.sensors_nodes = []
        self.smart_meters_nodes = []
        self.actuators_nodes = []
        self.access_points_nodes = []

        self.__addAccessPoints__()

        self.__addNodes__()

        server = self.net.addHost(
            'fog-server', mac='00:00:00:00:08:00', ip='10.10.10.254/8')

        self.switch = self.net.addSwitch('sw',  dpid=self.__int2dpid__(1))

        self.controller = self.net.addController('cl', controller=Controller)

        self.net.setPropagationModel(model="logDistance", exp=4)

        info("*** Configuring wifi nodes\n")
        self.net.configureWifiNodes()
        self.net.plotGraph(max_x=self.max_x, max_y=self.max_y)

        info("*** Enabling Association control (AP)\n")
        self.net.auto_association()

        info("*** Creating links and associations\n")
        self.net.addLink(self.switch, server)
        for ap in self.access_points_nodes:
            self.net.addLink(ap, self.switch)

    def start(self):
        self.net.build()
        self.controller.start()
        self.switch.start([self.controller])

        for ap in self.access_points_nodes:
            ap.start([self.controller])

        self.__start_actuator_server__()
        self.__start_fog_server__()
        
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

    def __addNodes__(self, network='10.0.0.0/8'):
        """
            creates nodes and add it to mininet.net object which contain all spawned network devices.
        """
        control = 0
        total = self.sensors + self.smart_meters + self.actuators

        coordinates = self.__generateNodesCoordinates__(
            radius=100, reference=(100, 100))

        mac_addresses = self.__generateNodesMacAddress__()

        network = IPNetwork(network)

        add_hosts = ((total//255) * 2) + 255 // (total % 255)
        ip_addresses = [str(network[i]) for i in range(total + add_hosts) if not str(
            network[i]).endswith('.0') and not str(network[i]).endswith('.255')]

        # create sensor nodes
        for i in range(self.sensors):
            control += 1
            device_name = 'sensor%d' % (i+1)
            pos = '%s,%s,0' % (coordinates[i][0], coordinates[i][1])
            mac_addr = mac_addresses[i]
            ip_addr = ip_addresses[i]

            print("Device: ", device_name, "ip_addr:",
                  ip_addr, "position:", pos)

            node = self.net.addStation(
                device_name, mac=mac_addr, ip=ip_addr, antennaHeight='1', antennaGain='5',  position=pos)

            self.sensors_nodes.append(node)

        # create smart meter nodes
        for i in range(self.smart_meters):
            device_name = 'meters%d' % (i+1)
            pos = '%s,%s,0' % (
                coordinates[control][0], coordinates[control][1])
            mac_addr = mac_addresses[control]
            ip_addr = ip_addresses[control]

            print("Device: ", device_name, "ip_addr:",
                  ip_addr, "position:", pos)

            node = self.net.addStation(
                device_name, mac=mac_addr, ip=ip_addr, antennaHeight='1', antennaGain='5',  position=pos)

            self.smart_meters_nodes.append(node)
            control += 1

        # create actuators nodes
        for i in range(self.actuators):
            device_name = 'actuator%d' % (i+1)
            pos = '%s,%s,0' % (
                coordinates[control][0], coordinates[control][1])
            mac_addr = mac_addresses[control]
            ip_addr = ip_addresses[control]

            print("Device: ", device_name, "ip_addr:",
                  ip_addr, "position:", pos)

            node = self.net.addStation(
                device_name, mac=mac_addr, ip=ip_addr, antennaHeight='1', antennaGain='5',  position=pos)

            self.actuators_nodes.append(node)
            control += 1

    def __addAccessPoints__(self):
        ap1 = self.net.addAccessPoint(
            'ap1', ssid='iGrid-ap1', mode='g', channel='6', model='DI524', position='50,125,0', range='100')
        self.access_points_nodes.append(ap1)

        ap2 = self.net.addAccessPoint(
            'ap2', ssid='iGrid-ap2', mode='g', channel='1', model='DI524', position='100,75,0', range='100')
        self.access_points_nodes.append(ap2)

        ap3 = self.net.addAccessPoint('ap3', ssid='iGrid-ap3', mode='g',
                                      channel='3', model='DI524', position='125,125,0', range='100')
        self.access_points_nodes.append(ap3)

    def __generateNodesCoordinates__(self, radius, reference=(0, 0)):
        """
            generates a random station x, y coordinate which lies within the AP coverage radius
            and returns its X and Y coordinates as a tuple.
        """
        coordinates = []

        total_nodes = self.sensors + self.smart_meters + self.actuators
        for _ in range(0, total_nodes):
            r = radius * math.sqrt(random())
            theta = 2 * math.pi * random()
            coordinates.append((round(
                reference[0] + r * math.cos(theta)), round(reference[1] + r * math.sin(theta))))
        return coordinates

    def __generateNodesMacAddress__(self):
        """
            Returns a completely random Mac Addresses
        """
        mac_addr = []
        total = self.sensors + self.smart_meters + self.actuators
        for _ in range(total):
            mac = [0x00, 0x16, 0x3e, randint(0x00, 0x7f), randint(
                0x00, 0xff), randint(0x00, 0xff)]
            mac_addr.append(':'.join(map(lambda x: "%02x" % x, mac)))
        return mac_addr

    def __start_fog_server__(self):
        server = self.net.get('fog-server')
        server.cmd('nohup python sockets/server.py %s &' % server.IP())

    def __start_actuator_server__(self):
        for node in self.actuators_nodes:
            node.cmd('nohup python sockets/server.py %s &' % node.IP())
