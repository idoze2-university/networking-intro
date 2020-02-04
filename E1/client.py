import re
from socket import socket, AF_INET, SOCK_DGRAM
import sys


def get_port():
    default_port = 12345
    port = default_port
    try:
        port = int(sys.argv[1])
    except:
        print '** No port specified, using default.'
    return port


if __name__ == '__main__':
    s = socket(AF_INET, SOCK_DGRAM)
    dest_port = get_port()
    dest_ip = '127.0.0.1'
    msg = raw_input("> ")
    while msg is not 'quit':
        if msg:
            if int(re.search(r'\d+', msg).group()) in range(1, 6):
                s.sendto(msg, (dest_ip, dest_port))
                data, sender_info = s.recvfrom(2048)
                try:
                    head, body = data.split(' ', 1)
                except:
                    head, body = data, None
                if head != msg[0]:
                    print '** Some error occured on server side, please try again.'
                if body:
                    print body

            else:
                print 'illegal input'
        msg = raw_input("> ")
    s.close()
