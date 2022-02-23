from traceback import format_exc as f_exc
from server.tools import report
import threading
import os
import socket
import select
from .handler import Request_Abstract


# consts
MAX_BUFFER_LIMIT = 16000


class Base_Manager:
    reporter = report.Log()
    levels = [reporter.debug, reporter.info, reporter.warning, reporter.error, reporter.critical]
    threads = []

    def __del__(self):
        for thread_name in self.threads:
            thread_name.join()
            
        self.threads.clear()


    def write_log(self, msg, level):
        self.reporter.report(msg, self.levels[level - 1])


    def execute_thread(self, function, daemon=False, *args, **kwargs):
        threading.Thread(target=function, daemon=daemon, *args, **kwargs).start()



class Server(socket.socket, Base_Manager):
    def __init__(self, callback, ip_address="localhost", port=5000):
        self.ip_address = ip_address
        self.port = port

        # socket initialization
        super().__init__(socket.AF_INET, socket.SOCK_STREAM)
        super(Base_Manager).__init__()

        self.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        # flags and vars
        self.is_started = False
        self.sockets_r = [self]      # list of all socket to be read including server socket itself
        self.sockets_w = [self]      # list of all socket to be wrote including server socket itself
        self.sockets_err = [self]    # list of all socket to be write error including server socket itself
        self.sockets_info = {}       # list of all client socket and their basic information
        self.callback = callback     # called when receive incoming request

    def __del__(self):
        self.sockets_w.clear()
        self.sockets_r.clear()
        self.sockets_err.clear()
        self.sockets_info.clear()
        self.close()


    def bind_server(self, max_backlog=5):
        try:
            self.bind((self.ip_address, self.port))
            self.listen(max_backlog)
            self.is_started = True
            self.write_log(f"Server is on-air {self.ip_address}:{self.port}", 1)

        except:
            self.write_log(f_exc(), 5)


    def accept_connection(self):
        try:
            sock_, addr = self.accept()
            self.sockets_r.append(sock_)
            self.sockets_info[sock_] = {}
            self.sockets_info[sock_]["address"] = addr
            return sock_

        except:
            self.write_log(f_exc(), 5)


    def send_data(self, socket_, header, content, file_type=False):
        """
        send content trough the stream

        if :file_type is true then it will be send a file instead of regular data
        and send the content of given io handler
        """
        try:
            socket_.send(header)

            if file_type:
                self.sendfile()
                return socket_.sendfile(content)

            return socket_.send(content)

        except:
            self.write_log(f_exc(), 5)


    def receive_data(self, socket_, buffer_limit=MAX_BUFFER_LIMIT):
        """
        returns decoded data from given socket object

        if the header is exceed than given buffer limit then
        there is a guarantee that data may be truncated
        """
        
        try:
            data_ = socket_.recv(buffer_limit)

            if not data_:
                return ""

            return data_.decode()

        except:
            self.write_log(f_exc(), 5)


    def halt(self):
        if not self.is_started:
            return "Server is already disabled!"

        self.is_started = False
        self.sockets_r.pop(0)

        for client_socket in self.sockets_r:
            self.dispatch_connection(client_socket)

    
    def dispatch_connection(self, socket_):
        try:
            self.write_log(f"{socket_.getpeername()} just disconnected!", 1)
            socket_.close()
            self.sockets_r.remove(socket_)
            del self.sockets_info[socket_]


        except:
            self.write_log(f_exc(), 5)


    def start(self):
        if not self.is_started:
            return "Server is not running yet!"

        while self.is_started:
            try:
                for incoming_socket in select.select(self.sockets_r, self.sockets_w, self.sockets_err):
                    if not incoming_socket:
                        continue

                    if incoming_socket[0] == self:
                        header_ = self.receive_data(self.accept_connection())

                    else:
                        header_ = self.receive_data(incoming_socket[0])

                    if not header_:
                        # client just disconnected
                        self.dispatch_connection(incoming_socket[0])
                        continue

                    if callable(self.callback):
                        self.callback(self, Request_Abstract(header_, incoming_socket[0]))


            except KeyboardInterrupt:
                # ask to halt the server
                self.execute_thread(self.halt)

            except:
                self.write_log(f_exc(), 5)
            
