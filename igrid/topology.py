from mininet.node import Controller
from mn_wifi.net import Mininet_wifi
from mn_wifi.link import wmediumd
from mn_wifi.node import OVSKernelAP
from mininet.log import setLogLevel, info


class IGRID:
    net = Mininet_wifi(controller=Controller, link=wmediumd,
                       accessPoint=OVSKernelAP, noise_th=-91,  ac_method='sf')

    def __init__(self, sensors=0, smart_meters=0, actuator=0):
        self.sensors = []
        self.smart_meters = []
        self.actuator = []

        # add access points
        ap1 = self.net.addAccessPoint(
            'ap1', ssid='iGrid-ap1', mode='g', channel='6', model='DI524', position='50,125,0', range='100')
        ap2 = self.net.addAccessPoint(
            'ap2', ssid='iGrid-ap2', mode='g', channel='1', model='DI524', position='100,75,0', range='100')
        ap3 = self.net.addAccessPoint('ap3', ssid='iGrid-ap3', mode='g',
                                      channel='3', model='DI524', position='125,125,0', range='100')

        server = self.net.addHost(
            'server', mac='00:00:00:00:08:00', ip='10.10.10.254/8')
        sw = self.net.addSwitch('sw',  dpid=self.int2dpid(1))

        cl = self.net.addController('cl', controller=Controller)

        self.net.setPropagationModel(model="logDistance", exp=4)

        # net.setModule('./mac80211_hwsim.ko')
        info("*** Configuring wifi nodes\n")
        self.net.configureWifiNodes()
        self.net.plotGraph(max_x=200, max_y=200)

        info("*** Enabling Association control (AP)\n")

        self.net.auto_association()

        info("*** Creating links and associations\n")
        self.net.addLink(ap1, sw)
        self.net.addLink(ap2, sw)
        self.net.addLink(ap3, sw)

        self.net.addLink(sw, server)

        info("*** Starting network\n")
        self.net.build()
        cl.start()
        ap1.start([cl])
        ap2.start([cl])
        ap3.start([cl])
        sw.start([cl])

    def int2dpid(self, dpid):
        try:
            dpid = hex(dpid)[2:]
            dpid = '0' * (16 - len(dpid)) + dpid
            return dpid
        except IndexError:
            raise Exception('Unable to derive default datapath ID - '
                            'please either specify a dpid or use a '
                            'canonical switch name such as s23.')
