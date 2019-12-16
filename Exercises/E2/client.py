import re
from socket import socket, AF_INET, SOCK_DGRAM
import sys

# Constant Variables####################
CLIENT_MODE_LISTENING = 0  # type: int
CLIENT_MODE_USER = 1  # type: int
CLIENT_MODES = [CLIENT_MODE_LISTENING, CLIENT_MODE_USER]
DEF_CLIENT_MODE = CLIENT_MODE_USER  # type: int
DEF_SERVER_IP = '192.168.1.21'  # type: str
DEF_SERVER_PORT = 12345  # type: int
########################################

if __name__ == '__main__':
    s = socket(AF_INET, SOCK_DGRAM)
    client_mode = (int(sys.argv[1]) if (sys.argv[1] in CLIENT_MODES) else DEF_CLIENT_MODE) if len(
        sys.argv) > 0 else DEF_CLIENT_MODE
    dest_ip = sys.argv[2] if len(sys.argv) > 1 else DEF_SERVER_IP
    dest_port = int(sys.argv[3]) if len(sys.argv) > 2 else DEF_SERVER_PORT

    s.bind((dest_ip, dest_port))
    msg = raw_input("")
    while msg != "quit":
        if msg:
            exp = re.search(r'\d+', msg)
            if int(exp.group() if exp else 0) in range(1, 6):  # if msg has a number in in [1,6]
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
        msg = raw_input("")
    s.close()
