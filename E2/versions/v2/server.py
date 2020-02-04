import socket,sys

TCP_IP = '0.0.0.0'
TCP_PORT = 12345
BUFFER_SIZE = 5

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((TCP_IP, TCP_PORT))
s.listen(1)

while True:
	conn, addr = s.accept()
	print 'New connection from:', addr
	while True:
	    data = conn.recv(BUFFER_SIZE)
	    if not data: break
	    print "received:", data
	    conn.send(data.upper()) 
	conn.close()
