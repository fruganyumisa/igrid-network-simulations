import random
import schedule
import itertools
import threading
from scapy.all import *
from topology import IGRID
from multiprocessing import Pool


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

    def __batch_schedule__(self, batch=[], interval=1, dst={}):
        for i in batch:
            schedule.every(interval=interval).seconds.do(
                job_func=self.__send_packet__, srip=i, destination=dst).tag("sim")

    def __split_nodes__(self, alist, wanted_parts=1):
        random.shuffle(alist)
        length = len(alist)
        return [alist[i*length // wanted_parts: (i+1)*length // wanted_parts]
                for i in range(wanted_parts)]

    def send_once(self, port=8080):

        dst = {"ip": self.net.get('fog-server').IP(), "port": port}

        # sensors nodes send traffic
        pool = Pool(processes=len(self.sensors_nodes))
        pool.map(self.__unpack_send_packet__, itertools.izip(
            self.sensors_nodes, itertools.repeat(dst)))
        pool.close()

        time.sleep(20)

        # smart meter nodes send trafic
        pool = Pool(processes=len(self.smart_meters_nodes))
        pool.map(self.__unpack_send_packet__, itertools.izip(
            self.smart_meters_nodes, itertools.repeat(dst)))
        pool.close()

        time.sleep(5)

        # actuator nodes receive traffic from for server
        pool = Pool(processes=len(self.actuators_nodes))
        pool.map(self.__unpack_send_packet__, itertools.izip(
            itertools.repeat(dst), self.actuators_nodes))
        pool.close()

    def send_in_interval(self, port):
        dst = {"ip": self.net.get('fog-server').IP(), "port": port}

        nodes = [node for node in itertools.chain(
            self.sensors_nodes, self.smart_meters_nodes)]
        nodes_parts = self.__split_nodes__(alist=nodes, wanted_parts=10)

        interval = 5
        for part in nodes_parts:
            threading.Thread(target=self.__batch_schedule__, args=(
                part, interval, dst)).start()
            interval = +5

        while True:
            schedule.run_pending()
