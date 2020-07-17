#from packets import *
import time
from packets import unpack_send_packet, send_packet
from multiprocessing import Pool
import itertools
import signal
import sys
import schedule
import random
import threading

def generate_ip(start_ip=1, total_ips=25,):
    ip_array = []
    for ip in range(total_ips):
        ip_prefix = '10.0.0'
        start_ip = start_ip+1
        current_ip = '{}.{}'.format(ip_prefix, start_ip)
        ip_array.append(current_ip)

    return ip_array


def split_list(alist, wanted_parts=1):
    random.shuffle(alist)
    length = len(alist)
    return [alist[i*length // wanted_parts: (i+1)*length // wanted_parts]
            for i in range(wanted_parts)]


def batch_schedule(batch=[], interval=1, destination={}):
    for i in batch:
        schedule.every(interval=interval).seconds.do(job_func=send_packet, srip=i, destination=destination).tag("sim")


def node_send_in_interval():
    destination = {
        "ip": "10.0.0.55",
        "port": 8080
    }
    ips_parts = split_list(alist=generate_ip(start_ip=1, total_ips=75), wanted_parts=10)

    interval = 5
    for part in ips_parts:
        threading.Thread(target=batch_schedule, args=(part, interval,destination)).start()
        interval=+5

    while True:
        schedule.run_pending()


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
        "port": 8080
    }
    pool.map(unpack_send_packet, itertools.izip(generate_ip(
        start_ip=1, total_ips=30), itertools.repeat(destination)))
    pool.close()
    time.sleep(20)

    # stations(sensors) send their traffic
    pool = Pool(processes=45)
    pool.map(unpack_send_packet, itertools.izip(generate_ip(
        start_ip=31, total_ips=45), itertools.repeat(destination)))
    pool.close()
    time.sleep(5)

    # actuator receive the packets from fog
    pool = Pool(processes=10)
    pool.map(unpack_send_packet, itertools.izip(generate_ip(
        start_ip=76, total_ips=10), itertools.repeat(destination)))
    pool.close()


def signal_handler(sig, frame):
    print 'You pressed Ctrl+C!'
    schedule.clear(tag="sim")
    sys.exit(0)


if __name__ == "__main__":
    signal.signal(signal.SIGINT, signal_handler)
    # while True:
    #     node_sendpkts()
    node_send_in_interval()
