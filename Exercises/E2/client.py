import re, glob
import time
from socket import socket, AF_INET, SOCK_STREAM
import random
import sys

# Constant Variables####################
CLIENT_MODE_LISTENING = '0'  # type: int
CLIENT_MODE_USER = '1'  # type: int
CLIENT_MODES = [CLIENT_MODE_LISTENING, CLIENT_MODE_USER]
DEF_CLIENT_MODE = CLIENT_MODE_USER  # type: int
DEF_SERVER_IP = '192.168.1.21'  # type: str
DEF_SERVER_PORT = 12345  # type: int
DEF_LISTENING_IP = '0.0.0.0'  # type: str
DEF_LISTENING_PORT = random.randint(1000, 10000)  # type: int
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

    m = client_mode + ' '
    if client_mode == CLIENT_MODE_LISTENING:
        listening_port = int(sys.argv[4]) if len(sys.argv) > 4 else DEF_LISTENING_PORT
        m += str(listening_port) + ' '
        m += ','.join(glob.glob1("/home/idoz/University/Networking/Exercises/E2", "*.*"))
        s.send(m)
        data = s.recv(MAX_MSG_SIZE)
        if (data != '1'):
            print "Couldn't authenticate with server."
            exit(1)
        s.close()
        fs = socket(AF_INET, SOCK_STREAM)
        fs.bind((DEF_LISTENING_IP, listening_port))
        fs.listen(1)
        while (1):
            conn, sender = fs.accept()
            data = conn.recv(MAX_MSG_SIZE)
            print data
            f = open(data, "rb")
            l = f.read(MAX_MSG_SIZE)
            while (l):
                s.send(l)
                l = f.read(MAX_MSG_SIZE)
        fs.close()

    elif client_mode == CLIENT_MODE_USER:
        m += "\n"
        s.send(m)
        msg = raw_input("Search: ")
        while msg:
            s.send(msg)
            size, choices = s.recv(MAX_MSG_SIZE).split(';', 1)
            print size
            print choices
            if int(size):
                choice = 0
                try:
                    choice = raw_input("Choose: ")
                    if int(choice) in range(0, int(size)):
                        s.send(choice)
                        host_ip, host_port = s.recv(MAX_MSG_SIZE).split(':', 1)

                        print data
                    else:
                        raise 0
                except:
                    print "Illegal choice.\n"
            msg = raw_input("Search: ")
    s.close()
