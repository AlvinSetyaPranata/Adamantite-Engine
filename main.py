from server.core import Server
import os

def accept_request(cls, signal):
    # print(signal.get_method)
    print(signal.get_method_data)
    pass

d = Server(accept_request)
d.bind_server()
d.start()

