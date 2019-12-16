import sys, time
from socket import *
from typing import List, Any


class FileHost:
    def __init__(self, ip, port, listening_port):
        self.ip = ip
        self.port = port
        self.listening_port = listening_port

    def __str__(self):
        return self.ip + ':' + str(self.listening_port)

    ip = ''  # type: str
    port = 0  # type: int
    listening_port = 0  # type: int


class File:
    def __init__(self, name, host):
        self.name = name
        self.host = host

    name = ''  # type: str
    host = None  # type: FileHost

    def get_download_string(self):
        return self.name + ' ' + str(host)


# Constant Variables####################
CLIENT_MODE_LISTENING = 0  # type: int
CLIENT_MODE_USER = 1  # type: int
CLIENT_MODES = [CLIENT_MODE_LISTENING, CLIENT_MODE_USER]
DEF_IP = '0.0.0.0'  # type: str
DEF_PORT = 12345  # type: int
MAX_MSG_SIZE = 2048  # type: int
########################################

if __name__ == '__main__':
    port = int(sys.argv[1]) if len(sys.argv) > 1 else DEF_PORT
    s = socket(AF_INET, SOCK_STREAM)
    while (1):
        try:
            s.bind((DEF_IP, port))
            break
        except:
            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            time.sleep(0.0001)
    print "Connected to 12345\n"
    s.listen(10)

    files = []
    while True:
        conn, sender = s.accept()
        data = conn.recv(MAX_MSG_SIZE)
        if data:
            client_mode, body = data.split(' ', 1)
            if int(client_mode) == CLIENT_MODE_LISTENING:
                listening_port, file_list = body.split(' ', 1)
                host = FileHost(sender[0], sender[1], listening_port)
                for file_name in file_list.split(','):
                    files.append(File(file_name, host))
                time.sleep(1)
                try:
                    print 'just trying to send'
                    s.send('1')
                except:
                    print 'obby it failed, nvm.'
                    continue


            elif int(client_mode) == CLIENT_MODE_USER:
                continue

    s.close()
