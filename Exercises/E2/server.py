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
        return self.name + ':' + str(host)


# Constant Variables####################
CLIENT_MODE_LISTENING = 0  # type: int
CLIENT_MODE_USER = 1  # type: int
CLIENT_MODES = [CLIENT_MODE_LISTENING, CLIENT_MODE_USER]
DEF_IP = '0.0.0.0'  # type: str
DEF_PORT = 12345  # type: int
MAX_MSG_SIZE = 1024  # type: int
########################################

if __name__ == '__main__':
    port = int(sys.argv[1]) if len(sys.argv) > 1 else DEF_PORT
    s = socket(AF_INET, SOCK_STREAM)
    s.bind((DEF_IP, port))
    s.listen(1)

    files = []
    while True:
        try:
            conn, sender = s.accept()
            data = conn.recv(MAX_MSG_SIZE)
            if data:
                client_mode, body = data.split(' ', 1)
                if int(client_mode) == CLIENT_MODE_LISTENING:
                    listening_port, file_list = body.split(' ', 1)
                    host = FileHost(sender[0], sender[1], listening_port)
                    for file_name in file_list.split(','):
                        if file_name in list(f.name for f in files): # handles duplicate file names
                            files.remove(list(f for f in files if f.name == file_name)[0])
                        files.append(File(file_name, host))
                    conn.send('1')

                elif int(client_mode) == CLIENT_MODE_USER:
                    search_pattern = conn.recv(MAX_MSG_SIZE)
                    while search_pattern:
                        result_list = list(f for f in files if search_pattern in f.name)
                        result_list.sort(key=lambda f: f.name)
                        size = len(result_list);
                        search_result = str(size) + ';'
                        for i, f in enumerate(result_list):
                            search_result += str.format("{0} {1}\n", i + 1, f.name)
                        conn.send(search_result if search_result else "0;No results.\n")
                        if size:
                            choice = int(conn.recv(MAX_MSG_SIZE))
                            conn.send(str(result_list[choice - 1].get_download_string())) if choice else 0
                        search_pattern = conn.recv(MAX_MSG_SIZE)
        except:
            break

    s.close()
