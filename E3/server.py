import sys
import os
from socket import *

# Constants ############################
MSG_SUFFIX = "\r\n\r\n"
DEF_IP = '0.0.0.0'  # type: str
DEF_PORT = 12345  # type: int
MAX_MSG_SIZE = 1024  # type: int
CWD = os.getcwd()
status_code = {200: '200 OK',
               404: '404 Not Found',
               301: '301 Moved Permanently'}
translate = {'/': 'index.html',
             '/redirect': 'result.html'}
binary_extensions = ['ico', 'jpg', 'png']
########################################
if __name__ == '__main__':
    # Handle passing port number via cli argument.
    port = int(sys.argv[1]) if len(sys.argv) > 1 else DEF_PORT
    # Bind the socket and create settings.
    s = socket(AF_INET, SOCK_STREAM)
    s.bind((DEF_IP, port))
    s.settimeout(1000)
    s.listen(1)
    # Main logic loop.
    while True:
        conn, sender = s.accept()
        data = ""
        # Get all data from request.
        while not data.endswith(MSG_SUFFIX):
            data += conn.recv(MAX_MSG_SIZE)
        # Make sure data isn't empty
        if data:
            # Parse request. (Note, could be optimized by regex, seems redundant to disallow the use of regex.)
            _filename = data[data.find("GET ") + len("GET "):data.find(" HTTP/1.1")]
            data = data[data.find("Connection: "):len(data)]
            connection_header = data[len("Connection: "):data.find("\r")]
            # Find out if _filename has a known translation.
            try:
                _filename = translate[_filename]
            except KeyError as e:
                pass
            # Get the file specifier (suffix).
            file_suffix = _filename.split(".", 1)[1]
            # Initialize values for the various variables.
            status = 301 if _filename == "/result.html" else 200
            resp = ""
            content = ""
            # Try to find the file.
            try:
                _file = open(CWD + "/files/" + _filename, "rb" if file_suffix in binary_extensions else "r")
                file_content = ""
                while 1:
                    file_content = _file.read(MAX_MSG_SIZE)
                    content += file_content
                    if not file_content:
                        break
            except IOError as e:  # The file isn't found.
                status = 404
            # Compose a response to the client.
            resp += "HTTP/1.1 %s\r\n" % status_code[status]  # Each response starts with a status code.
            if status is 200:
                resp += "Connection: %s\r\n" % connection_header
                resp += str.format("Content-Length: %s%s" % (len(content), MSG_SUFFIX))
                resp += content if file_suffix in binary_extensions else content.encode()  # Make sure to encode data.

            elif status in [404, 301]:
                resp += "Connection: Close\r\n"  # Force connection to close here.

            if status is 301:
                resp += "Location %s%s" % (_filename, MSG_SUFFIX)  # Handle redirecting.
            conn.send(resp)  # Finally send an HTTP response.
    s.close()  # Close the socket -- unreachable code.
