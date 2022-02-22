from traceback import format_exc as f_exc
import os
import socket
import select
from server.tools import report

class Server(socket.socket):
    def __init__(self, ip_address=socket.gethostbyname(socket.gethostname()), port=5000):
        self.ip_address = ip_address
        self.port = port

        # socket initialization
        super().__init__(socket.AF_INET, socket.SOCK_STREAM)
        self.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        # flags and vars
        self.is_started = False
        self.sockets_r = [self]      # list of all socket to be read including server socket itself
        self.sockets_w = [self]      # list of all socket to be wrote including server socket itself
        self.sockets_err = [self]    # list of all socket to be write error including server socket itself
        self.sockets_info = {}       # list of all client socket and their basic information
        self.reporter = report.Log()

    def __del__(self):
        self.sockets_.clear()
        self.sockets_info.clear()
        self.close()

    def bind_server(self, max_backlog=5):
        try:
            self.bind((self.ip_address, self.port))
            self.listen(max_backlog)

        except:
            self.reporter.report(f_exc(), self.reporter.error)

    def halt(self):
        self.sockets_.pop(0)

        for client_socket in self.sockets_:
            self.send_data(client_socket, b"0x1")
            client_socket.close()

        

    def start(self):
        if not self.is_started:
            return "Server is not running yet!"

        while self.is_started:
            try:
                for incoming_socket in select.select(self.sockets_r, self.sockets_w, self.sockets_err):
                    if not incoming_socket:
                        continue

                    print(incoming_socket)

            except KeyboardInterrupt:
                # ask to halt the server
                pass

            except:
                self.reporter.report(f_exc(), self.reporter.error)
            
