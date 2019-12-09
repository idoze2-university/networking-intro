from socket import socket, AF_INET, SOCK_DGRAM
import sys
from typing import List, Any


class Member:
    def __init__(self, name, port):
        self.name = name
        self.port = port

    name = ''  # type: str
    port = 0  # type: int
    queue = list()  # type: List[str]

    def receive_message(self, msg):
        self.queue.append(msg)

    def get_queue(self):
        q = '\n'.join(list(self.queue))  # type: str
        self.queue = list()
        return q


def create_socket(port):
    s = socket(AF_INET, SOCK_DGRAM)
    s.bind(('0.0.0.0', int(port)))
    return s


def boldstr(s):
    return '\033[1m' + str(s) + '\033[0m'


def open_socket():
    default_port = 12345
    port = default_port
    try:
        port = int(sys.argv[1])
    except:
        print '** No port specified, using default.'
    try:
        s = create_socket(port)
    except:
        print '** Cannot establish connection on ' + boldstr(port) + ', using default.'
        port = default_port
        s = create_socket(port)
    print 'Connection established, listening on ' + boldstr(port)
    return s


if __name__ == '__main__':
    print 'Welcome to EZ-Chat Server!'
    errors = [
        "1 Please use \"3 [new_name]\" to change your name, you are already logged in."
        "2 Please use \"1 [name]\" to login before sending a message.",

    ]
    s = open_socket()
    members = []
    while True:
        data, sender_info = s.recvfrom(2048)
        user_port = sender_info[1]
        if data and sender_info:
            try:
                head, body = data.split(' ', 1)
            except:
                head, body = data, None
            get_messages = False
            response = ""
            member_sent = None
            # 1: Register
            if head == '1' and body:
                if member_sent:
                    response = errors[0]
                else:
                    new_member = Member(body, user_port)
                    msg = boldstr(body) + " has joined"
                    print(msg)
                    for member in members:
                        member.receive_message(msg)
                    members.append(new_member)
                    response = head
            # Assert user registration
            elif not (m for m in members if m.port == user_port):
                response = errors[1]
                s.sendto(response, sender_info)
            else:
                member_sent = filter(lambda m: m.port == user_port, members)[0]
                msg = ''
                # 2: Send a message
                # Make sure the message came from an existing user.
                if head == '2' and body:
                    msg = boldstr(member_sent.name) + ": " + str(body)

                # 3: Change name
                elif head == '3':
                    msg = boldstr(member_sent.name) + " changed his name to " + boldstr(body)
                    member_sent.name = body

                elif head == '4':
                    msg = boldstr(member_sent.name) + " has left"
                    members.remove(member_sent)
                    response = "4 logged out."

                if head in ['2', '3', '4']:
                    print(msg)
                    for member in members:
                        if(member is not member_sent):
                            member.receive_message(msg)

                if head in ['2', '3', '5']:
                    response = str.format("{0} {1}", head, member_sent.get_queue())

            s.sendto(response, sender_info)
    s.close()
