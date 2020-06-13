#!/usr/bin/python

from scapy.all import *
from utils import spawnStations


def create_packet(srip, dstip, dstport, payload='This is dummy traffic'):
    data = payload
    packet = Ether()/IP(src=srip, dst=dstip)/TCP(dport=dstport)/data

    return packet


def send_packet(srip, dsip, dstport, data="V = 240, I = 15, T = 08:40 PM V = 240, I = 15, T = 08:40 PM V = 240, I = 15, T = 08:40 PM V = 240, I = 15, T = 08:40 PM V = 240, I = 15, T = 08:40 PM V = 240, I = 15, T = 08:40 PM V = 240, I = 15, T = 08:40 PM V = 240, I = 15, T = 08:40 PM V = 240, I = 15, T = 08:40 PM V = 240, I = 15, T = 08:40 PM V = 240, I = 15, T = 08:40 PM V = 240, I = 15, T = 08:40 PM V = 240, I = 15, T = 08:40 PM V = 240, I = 15, T = 08:40 PM V = 240, I = 15, T = 08:40 PM V = 240, I = 15, T = 08:40 PM V = 240, I = 15, T = 08:40 PM V = 240, I = 15, T = 08:40 PM V = 240, I = 15, T = 08:40 PM"):
    packet = create_packet(srip=srip, dstip=dsip,
                           dstport=dstport, payload=data)
    send(packet, count=1, return_packets=True)


if __name__ == '__main__':
    send_packet(srip='127.0.0.1', dsip='8.8.8.8', dstport=53)
