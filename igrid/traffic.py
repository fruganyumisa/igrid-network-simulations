from scapy.all import *
from topology import IGRID


class Traffic(IGRID):

    def __init__(self, sensors=0, smart_meters=0, actuators=0):
        self.payload = "V = 240, I = 15, T = 08:40 PM V = 240, I = 15, T = 08:40 PM V = 240, I = 15, T = 08:40 PM V = 240, I = 15, T = 08:40 PM V = 240, I = 15, T = 08:40 PM V = 240, I = 15, T = 08:40 PM V = 240, I = 15, T = 08:40 PM V = 240, I = 15, T = 08:40 PM V = 240, I = 15, T = 08:40 PM V = 240, I = 15, T = 08:40 PM V = 240, I = 15, T = 08:40 PM V = 240, I = 15, T = 08:40 PM V = 240, I = 15, T = 08:40 PM V = 240, I = 15, T = 08:40 PM V = 240, I = 15, T = 08:40 PM V = 240, I = 15, T = 08:40 PM V = 240, I = 15, T = 08:40 PM V = 240, I = 15, T = 08:40 PM V = 240, I = 15, T = 08:40 PM"
        super().__init__(sensors, smart_meters, actuators)

    def __create_packet__(self, src, dst, port, payload):
        return Ether()/IP(src=src, dst=dst)/TCP(dport=port)/payload

    def __send_packet__(self, src, dst={}):
        packet = self.__create_packet__(src=src, dst=dst.get(
            "ip"), port=dst.get("port"), payload=self.payload)
        send(packet, count=1, return_packets=True)

    def __unpack_send_packet__(self, args):
        self.__send_packet__(*args)
    
    
    