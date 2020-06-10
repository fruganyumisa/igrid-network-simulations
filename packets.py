#!/usr/bin/python

from scapy.all import *
from utils import spawnStations


def create_packet(srip, dstip, dstport):
    payload = "Dummy packets for igrid networks by Mr Chugulu Godfrey"
    packet = Ether()/IP(src=srip, dst=dstip)/TCP(dport=dstport)/ICMP()

    return packet

def send_packet(srip, dsip, dstport):
    packet = create_packet(srip=srip, dstip=dsip, dstport=dstport)
    sr(packet, count=10, return_packets=True)



if __name__ == '__main__':
    send_packet(srip='127.0.0.1', dsip='8.8.8.8', dstport=53)


