import re, glob
import time
from socket import socket, AF_INET, SOCK_STREAM
import sys

# Constant Variables####################
CLIENT_MODE_LISTENING = '0'  # type: int
CLIENT_MODE_USER = '1'  # type: int
CLIENT_MODES = [CLIENT_MODE_LISTENING, CLIENT_MODE_USER]
DEF_CLIENT_MODE = CLIENT_MODE_USER  # type: int
DEF_SERVER_IP = '192.168.1.21'  # type: str
DEF_SERVER_PORT = 12345  # type: int
DEF_LISTENING_IP = '0.0.0.0'  # type: str
DEF_LISTENING_PORT = 12223  # type: int
MAX_MSG_SIZE = 2048  # type: int
########################################

if __name__ == '__main__':
    s = socket(AF_INET, SOCK_STREAM)
    client_mode = sys.argv[1] if len(sys.argv) > 1 and (sys.argv[1] in CLIENT_MODES) else DEF_CLIENT_MODE
    dest_ip = sys.argv[2] if len(sys.argv) > 2 else DEF_SERVER_IP
    dest_port = int(sys.argv[3]) if len(sys.argv) > 3 else DEF_SERVER_PORT
    try:
        s.connect((dest_ip, dest_port))
    except:
        print str.format("Please make sure server {0}:{1} is open.", dest_ip, dest_port)
        exit(1)

    if client_mode == CLIENT_MODE_LISTENING:
        listening_port = int(sys.argv[4]) if len(sys.argv) > 4 else DEF_LISTENING_PORT
        m = client_mode + ' '
        m += str(listening_port) + ' '
        m += ','.join(glob.glob1("/home/idoz/University/Networking/Exercises/E2", "*.*")) + "\n"
        s.send(m)
        time.sleep(1)
        data = s.recv(MAX_MSG_SIZE)
        print data
        file_socket = socket(AF_INET, SOCK_STREAM)
        file_socket.bind((DEF_LISTENING_IP, listening_port))
        file_socket.listen(1)
        while True:
            continue

    elif client_mode == CLIENT_MODE_USER:
        msg = raw_input("Search: ")
        while msg:
            s.send(msg + "\n")
            data = s.recvfrom(MAX_MSG_SIZE)
            data = data.split(',')
        msg = raw_input("Search: ")
    s.close()
