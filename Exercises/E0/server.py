from socket import socket, AF_INET, SOCK_DGRAM
s = socket(AF_INET, SOCK_DGRAM)
source_ip = '0.0.0.0'
source_port = 12345
s.bind((source_ip, source_port))
while True:
 data, sender_info = s.recvfrom(2048)
 print "Message: ", data, " from: ", sender_info
 s.sendto(data.upper(), sender_info)
