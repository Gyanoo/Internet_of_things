import socket

MCAST_GRP = "236.0.0.0"
MCAST_PORT = 3456

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 2)    


while True:
    line = input('Prompt ("stop" to quit): ')
    if line == 'stop':
        break
    print('SENT: "%s"' % line)
    sock.sendto(line.encode('utf-8'), (MCAST_GRP, MCAST_PORT))
