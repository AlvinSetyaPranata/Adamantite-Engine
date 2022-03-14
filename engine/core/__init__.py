from adamantite.engine.core.controller import Controller
from adamantite.engine.handlers.http_ import HttpRequest, HttpResponse
from traceback import format_exc as f_exc
from socket import (
    socket, SOL_SOCKET, SO_REUSEADDR, SHUT_RDWR, AF_INET, SOCK_STREAM
)
from select import select as select_sock


class Server(Controller):
    def __init__(self, used_settings, callback, report=print):
        
        # socket initialization

        self.__server_sock_ = socket(AF_INET, SOCK_STREAM)
        self.__server_sock_.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        self.__used_settings = used_settings


        # flags and vars
        self.is_started = False
        self.sockets_list = [self.__server_sock_]       # list of all socket to be read including server socket itself
        self.callback = callback                        # called when HttpRequest and HttpResponse is generated and procesed 

        super().__init__(self.__used_settings ,callback, self.sockets_list ,report)


    def __del__(self):
        if not self.is_started:
            return

        self.sockets_list.clear()
        self.__server_sock_.shutdown(SHUT_RDWR)
        self.__server_sock_.close()


    def bind_server(self):
        max_backlog = self.__used_settings["MAX_BACKLOG"]
        ip_, port_ = self.__used_settings["HOST"].split(":")

        try:
            self.__server_sock_.bind((ip_, int(port_)))

            if max_backlog == "unlimited":
                self.__server_sock_.listen()
            else:
                self.__server_sock_.listen(int(max_backlog))
                
            self.is_started = True
            self.report(f"Server is on-air {ip_}:{port_}", 1)
            

        except:
            self.report(f_exc(), 5)


    def accept_connection(self, sock_):
        try:
            sock_, addr = sock_.accept()
            self.report(f"New Connection from {addr} Has ben Established!", 1)
            return sock_

        except:
            self.report(f_exc(), 5)


    def receive_data(self, socket_, buffer_limit="default", on_none=None):
        """
        :on_none = execute given function if client doenst respond / close the connection
        """
        if buffer_limit == "default":
            buffer_limit = int(self.__used_settings["MAX_BUFFER_LIMIT"])

        try:
            data_ = socket_.recv(buffer_limit)

            if not data_:
                if on_none:
                    on_none(socket_)

                return ""
                

            return data_.decode()

        except IOError:
            return ""

        except KeyboardInterrupt:
            self.halt()

        except:
            self.report(f_exc(), 5)


    def halt(self):
        if not self.is_started:
            self.report(f_exc(), 5)

        self.is_started = False

        for client_socket in self.sockets_list:
            if client_socket != self.__server_sock_:
                self.dispatch_connection(client_socket)

    
    def dispatch_connection(self, socket_):
        try:
            if len(self.sockets_list) == 1:
                return

            elif socket_ == self.__server_sock_:
                if socket_ in self.read_sockets:
                    self.read_sockets.remove(socket_)
                return


            socket_.close()
            self.sockets_list.remove(socket_)


        except:
            self.report(f_exc(), 5)



    def start(self):
        if not self.is_started:
            self.report("Server is not running yet!", 3)

        while self.is_started:
            fd_pointer = 0
            try:
                for incoming_socket in select_sock(self.sockets_list, self.sockets_list, self.sockets_list):
                    if not incoming_socket:
                        continue


                    if incoming_socket[0] == self.__server_sock_:
                        c_socket = self.accept_connection(incoming_socket[0])
                        received_header = self.receive_data(c_socket, on_none=self.dispatch_connection)

                    else:
                        c_socket = incoming_socket[0]
                        received_header = self.receive_data(c_socket, on_none=self.dispatch_connection)


                    if not received_header:
                        continue

                    self.read_sockets.append(c_socket)
                    
                    self.create_executor(HttpRequest(received_header), c_socket, HttpResponse())

                    fd_pointer += 1


            except KeyboardInterrupt:
                self.halt()

                
            except ValueError as e:
                # usally caused by file descriptor that have value bellow 0
                self.dispatch_connection(self.read_sockets[fd_pointer])         
