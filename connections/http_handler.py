import usocket

class Server:

    def __init__(self, address=('0.0.0.0', 80)):
        # max package length for every recv
        self._MAX_PACKET = 2048

        # socket initialization
        self._server_socket = usocket.socket(usocket.AF_INET, usocket.SOCK_STREAM, usocket.IPPROTO_TCP)
        self._server_socket.bind(address)
        self._server_socket.listen(1)

    def get_body(self):
        return '''<html>
<body>

<h2>Add a new network</h2>

<form method="post">
  <label for="ssid">SSID:</label><br>
  <input type="text" id="ssid" name="ssid" value=""><br>
  <label for="password">Password:</label><br>
  <input type="password" id="password" name="password" value=""><br><br>
  <input type="submit" value="Submit">
</form> 


</body>
</html>'''

    def recv_all(self, sock):
        try:
            sock.settimeout(0.1)
            rdata = []
            while True:
                try:
                    rdata.append(sock.recv(self._MAX_PACKET).decode('utf-8'))
                except OSError:
                    return ''.join(rdata)
        finally:
            sock.settimeout(0)

    def normalize_line_endings(self, text):
        return ''.join((line + '\n') for line in text.splitlines())

    def serve_one(self):
        try:
            client_sock, client_addr = self._server_socket.accept()

            request = self.normalize_line_endings(self.recv_all(client_sock))

            request_head, request_body = request.split('\n\n', 1)

            request_head = request_head.splitlines()
            request_headline = request_head[0]

            request_headers = dict(x.split(': ', 1) for x in request_head[1:])

            request_method, request_uri, request_proto = request_headline.split(' ', 3)

            new_network = None
            if request_method.lower() == 'get':
                response_body_raw = self.get_body()
            elif request_method.lower() == 'post':
                req_dict = {item.split('=')[0]:item.split('=')[1] for item in request_body.strip().split('&')}
                new_network = (req_dict['ssid'], req_dict['password'])
                response_body_raw = '<html>\n\n<body>\n\nDone.\n\n</body>\n\n</html>'
            else:
                response_body_raw = '<html>\n\n<body>\n\nMethod %s not supported.\n\n</body>\n\n</html>' % request_method

            # Clearly state that connection will be closed after this response,
            # and specify length of response body
            response_headers = {
                'Content-Type': 'text/html; encoding=utf8',
                'Content-Length': len(response_body_raw),
                'Connection': 'close',
            }

            response_headers_raw = ''.join('%s: %s\n' % (k, v) for k, v in \
                                                    response_headers.items())

            # Reply as HTTP/1.1 server, saying "HTTP OK" (code 200).
            response_proto = 'HTTP/1.1'.encode()
            response_status = '200'.encode()
            response_status_text = 'OK'.encode() # this can be random

            # sending all this stuff
            client_sock.send(b'%s %s %s' % (response_proto, response_status, response_status_text))
            client_sock.send(response_headers_raw.encode())
            client_sock.send(b'\n') # to separate headers from body
            client_sock.send(response_body_raw.encode())

        # and closing connection, as we stated before
        finally:
            client_sock.close()

        return new_network

    def get_new_credentials(self):
        new_network = None

        while not new_network:
            try:
                new_network = self.serve_one()
            except:
                pass
        # supposing the ssid and the password do not have any space
        return new_network

