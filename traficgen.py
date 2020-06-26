#from packets import *
import time
from packets import unpack_send_packet
from multiprocessing import Pool
import itertools


def generate_ip(start_ip=1, total_ips=25,):
    ip_array = []
    for ip in range(total_ips):
        ip_prefix = '10.0.0'
        start_ip = start_ip+1
        current_ip = '{}.{}'.format(ip_prefix, start_ip)
        print(start_ip)
        ip_array.append(current_ip)
        print(ip_array[ip])

    return ip_array


def node_sendpkts():
    """
This fuction generates ips from a given number from specified starting last octet number
@start_ip is the number to start when generating an ip
@total_ips is the number of the ips to be generated

"""

    # smartmeters send their traffic
    pool = Pool(processes=30)
    destination = {
        "ip": "10.0.0.55",
        "port": "8080"
    }
    pool.map(unpack_send_packet, itertools.izip(generate_ip(
        start_ip=1, total_ips=30), itertools.repeat(destination)))

    time.sleep(20)

    # stations(sensors) send their traffic
    pool = Pool(processes=45)
    pool.map(unpack_send_packet, itertools.izip(generate_ip(
        start_ip=31, total_ips=45), itertools.repeat(destination)))
    time.sleep(5)

    # actuator receive the packets from fog
    pool = Pool(processes=10)
    pool.map(unpack_send_packet, itertools.izip(generate_ip(
        start_ip=76, total_ips=10), itertools.repeat(destination)))


if __name__ == "__main__":
    node_sendpkts()
