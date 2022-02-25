from traceback import format_exc as f_exc
import threading
import os
import socket
import select


# consts
MAX_BUFFER_LIMIT = 16000


class Base_Manager:
    def __init__(self, report_to):
        self.threads = []
        self.report_to = report_to

    def __del__(self):
        for thread_name in self.threads:
            thread_name.join()
            
        self.threads.clear()

    def report(self, content, level):
        if not callable(self.report_to):
            if level > 4:
                raise Exception(content)

            return

        self.report_to(content, level)

    def execute_thread(self, function, daemon=False, *args, **kwargs):
        threading.Thread(target=function, daemon=daemon, *args, **kwargs).start()



class Server(Base_Manager):
    def __init__(self, callback, ip_address, port, report=None):
        """
        :report callback function must takes 2 argument from caller which is  (error_message, log_level) 
        if None then it will be run quitely. traceback might be raised if level is 4 or 5 (works only if in quite mode)
        """
        
        self.ip_address = ip_address
        self.port = port
        self.__server_sock_ = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # socket initialization
        super().__init__(report)

        self.__server_sock_.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        # flags and vars
        self.is_started = False
        self.sockets_r = [self.__server_sock_]      # list of all socket to be read including server socket itself
        self.sockets_w = [self.__server_sock_]      # list of all socket to be wrote including server socket itself
        self.sockets_err = [self.__server_sock_]    # list of all socket to be write error including server socket itself
        self.sockets_info = {}       # list of all client socket and their basic information
        self.callback = callback     # called when receive incoming request


    def __del__(self):
        self.sockets_w.clear()
        self.sockets_r.clear()
        self.sockets_err.clear()
        self.sockets_info.clear()
        self.__server_sock_.close()


    def bind_server(self, max_backlog=5):
        try:
            self.__server_sock_.bind((self.ip_address, self.port))
            self.__server_sock_.listen(max_backlog)
            self.is_started = True
            self.report(f"Server is on-air {self.ip_address}:{self.port}", 1)

        except:
            self.report(f_exc(), 5)


    def accept_connection(self):
        try:
            sock_, addr = self.__server_sock_.accept()
            self.sockets_r.append(sock_)
            self.sockets_info[addr] = {}
            self.sockets_info[addr]["socket"] = sock_
            return sock_

        except:
            self.report(f_exc(), 5)


    def send_data(self, socket_, header, content, file_type=False):
        """
        if :file_type is true then it will be send a file instead of regular data
        and send the content of given io handler
        """
        try:
            socket_.send(header)

            if file_type:
                return socket_.sendfile(content)

            return socket_.send(content)

        except:
            self.report(f_exc(), 5)


    def receive_data(self, socket_, buffer_limit=MAX_BUFFER_LIMIT):
        try:
            data_ = socket_.recv(buffer_limit)

            if not data_:
                return ""

            return data_.decode()

        except:
            self.report(f_exc(), 5)


    def halt(self):
        if not self.is_started:
            self.report(f_exc(), 5)

        self.is_started = False
        self.sockets_r.pop(0)

        for client_socket in self.sockets_r:
            self.dispatch_connection(client_socket)

    
    def dispatch_connection(self, socket_):
        try:
            socket_.close()
            self.sockets_r.remove(socket_)
            del self.sockets_info[socket_]


        except:
            self.report(f_exc(), 5)


    def start(self):
        if not self.is_started:
            raise Exception("Server is not running yet!")

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
                        self.callback(self, header_)


            except KeyboardInterrupt:
                # ask to halt the server
                self.execute_thread(self.halt)

            except:
                self.report(f_exc(), 5)
            
