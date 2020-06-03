#!/usr/bin/python

import time
from mininet.node import Controller
from mininet.log import setLogLevel, info
from mn_wifi.net import Mininet_wifi
from mn_wifi.node import OVSKernelAP
from mn_wifi.cli import CLI_wifi
from mn_wifi.devices import GetTxPower
from mn_wifi.link import wmediumd
from mn_wifi.wmediumdConnector import interference
from mn_wifi.propagationModels import propagationModel
from utils import spawnStations

# command to start virtual interface to capture simulations traffic
# sh ifconfig hwsim0 up





def int2dpid( dpid ):
   try:
      dpid = hex( dpid )[ 2: ]
      dpid = '0' * ( 16 - len( dpid ) ) + dpid
      return dpid
   except IndexError:
      raise Exception( 'Unable to derive default datapath ID - '
                       'please either specify a dpid or use a '
		       'canonical switch name such as s23.')


def topology():

    print("Welcome to mininet-Wifi")
    net = Mininet_wifi(controller = Controller, link=wmediumd, accessPoint =OVSKernelAP, noise_threshold=-91, fading_coefficient=3)


   ## Hey mbaga here the for loop should be placed you can create a function in which when called with input maybe number of AP3 it uses a loop to create them
    info("*** Creating nodes\n")
    ap1 = net.addAccessPoint('ap1', ssid= 'iGrid-ap1', mode = 'g', channel = '6',
    model='DI524', position = '10,30,0', range = '100')
    ap2 = net.addAccessPoint('ap2', ssid= 'iGrid-ap2', mode = 'g', channel = '1',
    model='DI524',position = '40,30,0', range = '100')
    ap3 = net.addAccessPoint('ap3', ssid= 'iGrid-ap3', mode = 'g', channel = '3',
    model='DI524', position = '60,30,0', range = '100')
   #  ap4 = net.addAccessPoint('ap4', ssid= 'iGrid-ap4', mode = 'g', channel = '4',
   #  model='DI524', position = '80,30,0', range = '20')
   #  ap5 = net.addAccessPoint('ap5', ssid= 'iGrid-ap5', mode = 'g', channel = '5',
   #  model='DI524', position = '10,0,0', range = '20')
   #  ap6 = net.addAccessPoint('ap6', ssid= 'iGrid-ap6', mode = 'g', channel = '6',
   #  model='DI524', position = '40,60,0', range = '20')
   #  ap7 = net.addAccessPoint('ap7', ssid= 'iGrid-ap7', mode = 'g', channel = '7',
   #  model='DI524', position = '40,0,0', range = '20')
   #  ap8 = net.addAccessPoint('ap8', ssid= 'iGrid-ap8', mode = 'g', channel = '8',
   #  model='DI524', position = '80,30,0', range = '20')
   #  ap9 = net.addAccessPoint('ap9', ssid= 'iGrid-ap9', mode = 'g', channel = '9',
   #  model='DI524', position = '80,0,0', range = '20')
   #  ap10 = net.addAccessPoint('ap10', ssid= 'iGrid-ap10', mode = 'g', channel = '10',
   #  model='DI524', position = '80,60,0', range = '20')

    # Creating Stations (Smart meters, sensors and actuators)


   ## Hey mbaga here the for loop should be placed you can create a function in which when called with input maybe number of particulr nodes
   #  it uses a loop to create them the nodes maybe the smart meters, sensors or actuators
     

    server = net.addHost('server', mac = '00:00:00:00:08:00', ip = '10.0.8.5/8')
    sw = net.addSwitch('sw',  dpid=int2dpid(1))

    net = spawnStations(net, stations=27, smart_meters=3, actuator=3, cidr="/8")

   #  smeter1 = net.addStation('smeter1', mac = '00:00:00:00:00:01', ip = '10.0.0.1/8',
   #  antennaHeight='1', antennaGain='5',position = '10,20,0',active_scan=1,scan_freq="2412 2437 2462")
   #  smeter2 = net.addStation('smeter2', mac = '00:00:00:00:00:02', ip = '10.0.0.2/8',
   #  antennaHeight='1', antennaGain='5',position = '28,30,0',active_scan=1,scan_freq="2412 2437 2462")
   #  smeter3 = net.addStation('smeter3', mac = '00:00:00:00:00:03', ip = '10.0.0.3/8',
   #  antennaHeight='1', antennaGain='5',  position = '10,40,0',active_scan=1,scan_freq="2412 2437 2462")
   #  actuator1 = net.addStation('actuator1', mac = '00:00:00:00:00:04', ip = '10.0.0.4/8',
   #  antennaHeight='1', antennaGain='5',  position = '50,40,0', active_scan=1,scan_freq="2412 2437 2462")
   #  actuator2 = net.addStation('actuator2', mac = '00:00:00:00:00:05', ip = '10.0.0.5/8',
   #  antennaHeight='1', antennaGain='5',  position = '50,40,0', active_scan=1,scan_freq="2412 2437 2462")
   #  actuator3 = net.addStation('actuator3', mac = '00:00:00:00:00:06', ip = '10.0.0.6/8',
   #  antennaHeight='1', antennaGain='5',  position = '50,40,0', active_scan=1,scan_freq="2412 2437 2462")
   #  sta7 = net.addStation('sta7', mac = '00:00:00:00:00:07', ip = '10.0.0.7/8',
   #  antennaHeight='1', antennaGain='5',  position = '50,40,0', active_scan=1,scan_freq="2412 2437 2462")
   #  sta8 = net.addStation('sta8', mac = '00:00:00:00:00:08', ip = '10.0.0.8/8',
   #  antennaHeight='1', antennaGain='5',  position = '50,40,0', active_scan=1,scan_freq="2412 2437 2462")
   #  sta9 = net.addStation('sta9', mac = '00:00:00:00:00:09', ip = '10.0.0.9/8',
   #  antennaHeight='1', antennaGain='5',  position = '50,40,0', active_scan=1,scan_freq="2412 2437 2462")
   #  sta10 = net.addStation('sta10', mac = '00:00:00:00:00:10', ip = '10.0.0.10/8',
   #  antennaHeight='1', antennaGain='5',  position = '50,40,0', active_scan=1,scan_freq="2412 2437 2462")
   #  sta11 = net.addStation('sta11', mac = '00:00:00:00:00:11', ip = '10.0.0.11/8',
   #  antennaHeight='1', antennaGain='5',  position = '50,40,0', active_scan=1,scan_freq="2412 2437 2462")
   #  sta12 = net.addStation('sta12', mac = '00:00:00:00:00:12', ip = '10.0.0.12/8',
   #  antennaHeight='1', antennaGain='5',  position = '50,40,0', active_scan=1,scan_freq="2412 2437 2462")
   #  sta13 = net.addStation('sta13', mac = '00:00:00:00:00:13', ip = '10.0.0.13/8',
   #  antennaHeight='1', antennaGain='5',  position = '50,40,0', active_scan=1,scan_freq="2412 2437 2462")
   #  sta14 = net.addStation('sta14', mac = '00:00:00:00:00:14', ip = '10.0.0.14/8',
   #  antennaHeight='1', antennaGain='5',  position = '50,40,0', active_scan=1,scan_freq="2412 2437 2462")
   #  sta15 = net.addStation('sta15', mac = '00:00:00:00:00:15', ip = '10.0.0.15/8',
   #  antennaHeight='1', antennaGain='5',  position = '50,40,0', active_scan=1,scan_freq="2412 2437 2462")
   #  sta16 = net.addStation('sta16', mac = '00:00:00:00:00:16', ip = '10.0.0.16/8',
   #  antennaHeight='1', antennaGain='5',  position = '50,40,0', active_scan=1,scan_freq="2412 2437 2462")
   #  sta17 = net.addStation('sta17', mac = '00:00:00:00:00:17', ip = '10.0.0.17/8',
   #  antennaHeight='1', antennaGain='5',  position = '50,40,0', active_scan=1,scan_freq="2412 2437 2462")
   #  sta18 = net.addStation('sta18', mac = '00:00:00:00:00:18', ip = '10.0.0.18/8',
   #  antennaHeight='1', antennaGain='5',  position = '50,40,0', active_scan=1,scan_freq="2412 2437 2462")
   #  sta19 = net.addStation('sta19', mac = '00:00:00:00:00:19', ip = '10.0.0.19/8',
   #  antennaHeight='1', antennaGain='5',  position = '50,40,0', active_scan=1,scan_freq="2412 2437 2462")
   #  sta20 = net.addStation('sta20', mac = '00:00:00:00:00:20', ip = '10.0.0.20/8',
   #  antennaHeight='1', antennaGain='5',  position = '50,40,0', active_scan=1,scan_freq="2412 2437 2462")
   #  sta21 = net.addStation('sta21', mac = '00:00:00:00:00:21', ip = '10.0.0.21/8',
   #  antennaHeight='1', antennaGain='5',  position = '50,40,0', active_scan=1,scan_freq="2412 2437 2462")
   #  sta22 = net.addStation('sta22', mac = '00:00:00:00:00:22', ip = '10.0.0.22/8',
   #  antennaHeight='1', antennaGain='5',  position = '50,40,0', active_scan=1,scan_freq="2412 2437 2462")
   #  sta23 = net.addStation('sta23', mac = '00:00:00:00:00:23', ip = '10.0.0.23/8',
   #  antennaHeight='1', antennaGain='5',  position = '50,40,0', active_scan=1,scan_freq="2412 2437 2462")
   #  sta24 = net.addStation('sta24', mac = '00:00:00:00:00:24', ip = '10.0.0.24/8',
   #  antennaHeight='1', antennaGain='5',  position = '50,40,0', active_scan=1,scan_freq="2412 2437 2462")
   #  sta25 = net.addStation('sta25', mac = '00:00:00:00:00:25', ip = '10.0.0.25/8',
   #  antennaHeight='1', antennaGain='5',  position = '50,40,0', active_scan=1,scan_freq="2412 2437 2462")
   #  sta26 = net.addStation('sta26', mac = '00:00:00:00:00:26', ip = '10.0.0.26/8',
   #  antennaHeight='1', antennaGain='5',  position = '50,40,0', active_scan=1,scan_freq="2412 2437 2462")
   #  sta27 = net.addStation('sta27', mac = '00:00:00:00:00:27', ip = '10.0.0.27/8',
   #  antennaHeight='1', antennaGain='5',  position = '50,40,0', active_scan=1,scan_freq="2412 2437 2462")
   #  sta28 = net.addStation('sta28', mac = '00:00:00:00:00:28', ip = '10.0.0.28/8',
   #  antennaHeight='1', antennaGain='5',  position = '50,40,0', active_scan=1,scan_freq="2412 2437 2462")
   #  sta29 = net.addStation('sta29', mac = '00:00:00:00:00:29', ip = '10.0.0.29/8',
   #  antennaHeight='1', antennaGain='5',  position = '50,40,0', active_scan=1,scan_freq="2412 2437 2462")
   #  sta30 = net.addStation('sta30', mac = '00:00:00:00:00:30', ip = '10.0.0.29/8',
   #  antennaHeight='1', antennaGain='5',  position = '50,40,0', active_scan=1,scan_freq="2412 2437 2462")
   #  sta31 = net.addStation('sta31', mac = '00:00:00:00:00:31', ip = '10.0.0.31/8',
   #  antennaHeight='1', antennaGain='5',  position = '50,40,0', active_scan=1,scan_freq="2412 2437 2462")
   #  sta32 = net.addStation('sta32', mac = '00:00:00:00:00:32', ip = '10.0.0.32/8',
   #  antennaHeight='1', antennaGain='5',  position = '50,40,0', active_scan=1,scan_freq="2412 2437 2462")
   #  sta33 = net.addStation('sta33', mac = '00:00:00:00:00:33', ip = '10.0.0.33/8',
   #  antennaHeight='1', antennaGain='5',  position = '50,40,0', active_scan=1,scan_freq="2412 2437 2462")
   #  sta34 = net.addStation('sta34', mac = '00:00:00:00:00:34', ip = '10.0.0.34/8',
   #  antennaHeight='1', antennaGain='5',  position = '50,40,0', active_scan=1,scan_freq="2412 2437 2462")



    cl = net.addController('cl', controller=Controller)
   

    #Takes 5 minutes before to proceed
    #time.sleep(40)
    net.setPropagationModel(model="logDistance", exp=4)



    info("*** Configuring wifi nodes\n")
    net.configureWifiNodes()
    
    #time.sleep(90)

    net.plotGraph(max_x=60, max_y=60)

    info("*** Enabling Association control (AP)\n")
    
    net.setAssociationCtrl(ac='ssf')
    net.auto_association()


    info("*** Creating links and associations\n")
    net.addLink(ap1, sw)
    net.addLink(ap2, sw)
    net.addLink(ap3, sw)
   #  net.addLink(ap4, sw)
   #  net.addLink(ap5, sw)
   #  net.addLink(ap6, sw)
   #  net.addLink(ap7, sw)
   #  net.addLink(ap8, sw)
   #  net.addLink(ap9, sw)
   #  net.addLink(ap10, sw)
    # net.addLink(ap1, sw)
    # net.addLink(ap1, sw)
    # net.addLink(ap1, sw)
    # net.addLink(ap1, sw)
    # net.addLink(ap1, sw)

    net.addLink(sw, server)
    #net.addLink(ap1, sta1)
    #net.addLink(ap2, sta2)
    #net.addLink(ap1,sta3)
    #net.addLink(ap2,sta4)

    info("*** Starting network\n")
    net.build()
    cl.start()
    ap1.start([cl])
    ap2.start([cl])
    ap3.start([cl])
  
    #  ap4.start([cl])
   #  ap5.start([cl])
   #  ap6.start([cl])
   #  ap7.start([cl])
   #  ap8.start([cl])
   #  ap9.start([cl])0.start([cl])

    info("*** Running CLI\n")
    CLI_wifi(net)

    
    x = 1

    while x>= 1:
       
       if (x%3 == 0):
          net.cmd('iperf smeter1 server')
       else:
         if(x%4 == 0):
            smeter1.cmd('iperf actuator1 server')
         else:
            smeter1.cmd('ping 10.0.8.5')


    


    info("*** Stopping the network \n")
    net.stop()

#setLogLevel('info')
#topology()

if __name__ == '__main__':
    setLogLevel('info')
    topology()