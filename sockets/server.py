import socket
import sys

address = (sys.argv[1], 8080)
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind(address)
f = open('/home/wifi/a.txt', 'w+')

while True:
    data, addr = s.recvfrom(1024)
    print 'data', data
    f.write(data)
    f.flush()
    f.close()
    s.close()
