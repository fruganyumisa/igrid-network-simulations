#!/usr/bin/python

from scapy.all import *
from utils import spawnStations


def create_packet(srip, dstip, dstport, payload='This is dummy traffic'):
    data = payload
    packet = Ether()/IP(src=srip, dst=dstip)/TCP(dport=dstport)/data

    return packet


def send_packet(srip, destination={}, data="V = 240, I = 15, T = 08:40 PM V = 240, I = 15, T = 08:40 PM V = 240, I = 15, T = 08:40 PM V = 240, I = 15, T = 08:40 PM V = 240, I = 15, T = 08:40 PM V = 240, I = 15, T = 08:40 PM V = 240, I = 15, T = 08:40 PM V = 240, I = 15, T = 08:40 PM V = 240, I = 15, T = 08:40 PM V = 240, I = 15, T = 08:40 PM V = 240, I = 15, T = 08:40 PM V = 240, I = 15, T = 08:40 PM V = 240, I = 15, T = 08:40 PM V = 240, I = 15, T = 08:40 PM V = 240, I = 15, T = 08:40 PM V = 240, I = 15, T = 08:40 PM V = 240, I = 15, T = 08:40 PM V = 240, I = 15, T = 08:40 PM V = 240, I = 15, T = 08:40 PM"):
    # packet = create_packet(srip=srip, dstip=destination.get("ip"),
    #                        dstport=destination.get("port"), payload=data)
    # send(packet, count=1, return_packets=True)
    print(srip, destination)


def unpack_send_packet(args):
    send_packet(*args)

