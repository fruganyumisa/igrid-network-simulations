#from packets import *
import time
from array import *
from packets import send_packet


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

    ip = generate_ip(start_ip=1, total_ips=50)

    for node in range(50):
        send_packet(ip[node], dsip='10.0.0.254', dstport=8080)

    time.sleep(20)
    # stations(sensors) send their traffic
    sensor_ip = generate_ip(start_ip=51, total_ips=90)

    for sensor in range(90):
        send_packet(sensor_ip[sensor], dsip='10.0.0.254', dstport=8080, data="V = 240, I = 15, T = 09:40")

    time.sleep(5)

    # actuator receive the packets from fog

    actuator_ip = generate_ip(start_ip=141, total_ips=10)

    for actuator in range(10):
        send_packet(srip='10.0.0.254', dsip=actuator_ip[actuator], dstport=8090, data="Close circuit")


if __name__ == "__main__":
    node_sendpkts()
