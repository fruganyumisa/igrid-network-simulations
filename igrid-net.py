#!/usr/bin/python

import time
from mininet.node import Controller
from mininet.log import setLogLevel, info
from mn_wifi.net import Mininet_wifi
from mn_wifi.node import OVSKernelAP
from mn_wifi.cli import CLI as CLI_wifi
from mn_wifi.devices import DeviceTxPower as GetTxPower
from mn_wifi.link import wmediumd
from mn_wifi.wmediumdConnector import interference
from mn_wifi.propagationModels import PropagationModel
from utils import spawnStations
from packets import *

# command to start virtual interface to capture simulations traffic
#





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
    net = Mininet_wifi(controller = Controller, link=wmediumd, accessPoint =OVSKernelAP, noise_th=-91,  ac_method='sf')


   ## Hey mbaga here the for loop should be placed you can create a function in which when called with input maybe number of AP3 it uses a loop to create them
    info("*** Creating nodes\n")
    ap1 = net.addAccessPoint('ap1', ssid= 'iGrid-ap1', mode = 'g', channel = '6',
    model='DI524', position = '10,30,0', range = '100')
    ap2 = net.addAccessPoint('ap2', ssid= 'iGrid-ap2', mode = 'g', channel = '1',
    model='DI524',position = '40,30,0', range = '100')
    ap3 = net.addAccessPoint('ap3', ssid= 'iGrid-ap3', mode = 'g', channel = '3',
    model='DI524', position = '60,30,0', range = '100')


    # Creating Stations (Smart meters, sensors and actuators)


   ## Hey mbaga here the for loop should be placed you can create a function in which when called with input maybe number of particulr nodes
   #  it uses a loop to create them the nodes maybe the smart meters, sensors or actuators
     

    server = net.addHost('server', mac = '00:00:00:00:08:00', ip = '10.0.8.5/8')
    sw = net.addSwitch('sw',  dpid=int2dpid(1))

    net = spawnStations(net, stations=27, smart_meters=3, actuator=3, cidr="/8")


    cl = net.addController('cl', controller=Controller)
   

    #Takes 5 minutes before to proceed
    #time.sleep(40)
    net.setPropagationModel(model="logDistance", exp=4)
    #net.setModule('./mac80211_hwsim.ko')



    info("*** Configuring wifi nodes\n")
    net.configureWifiNodes()
    server=net.start_socket(ip='10.0.8.5', port=8080)
    
    #time.sleep(90)

    net.plotGraph(max_x=300, max_y=300)

    info("*** Enabling Association control (AP)\n")
    
    
    net.auto_association()


    info("*** Creating links and associations\n")
    net.addLink(ap1, sw)
    net.addLink(ap2, sw)
    net.addLink(ap3, sw)
  

    net.addLink(sw, server)
  

    info("*** Starting network\n")
    net.build()
    cl.start()
    ap1.start([cl])
    ap2.start([cl])
    ap3.start([cl])

    #net.cmd( "sh ifconfig hwsim0 up")
    os.system("sh ifconfig hwsim0 up")
    os.system("sudo wireshark")
    time.sleep(10)


    info("Starting traffic\n")
    
    for i in range(27):
       device_control =+1
       ip_prefix ='10.0.0'
       srcip  = '{}.{}'.format(ip_prefix, device_control)
       dstip='10.0.8.5'
       dstport=8080

       send_packet(srip=srcip,dsip=dstip,dstport=dstport)
    

    
  
  

    info("*** Running CLI\n")
    CLI_wifi(net)

    
    x = 1

    while x>= 1:
       
       if (x%3 == 0):
          print("Not possible")
       else:
         if(x%4 == 0):
            print("Possible")
         else:
            print("NOt enough")


    


    info("*** Stopping the network \n")
    net.stop()

#setLogLevel('info')
#topology()

if __name__ == '__main__':
    setLogLevel('info')
    topology()