import os
import socket


class Server(socket.socket):
    def __init__(self, ip_address=socket.gethostbyname(socket.gethostname()), port=5000):
        self.ip_address = ip_address
        self.port = port

        # socket initialization
        super().__init__(socket.AF_INET, socket.SOCK_STREAM)
        self.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        # flags and vars
        self.started = False
        self.sockets_ = [self]      # list of all socket including server socket itself
        self.sockets_info = {}      # list of all client socket and their basic information


    def bind_server(self, max_backlog=5):
        try:
            self.bind((self.ip_address, self.port))
            self.listen(max_backlog)
            

        except:
            # report exception to log
            pass
