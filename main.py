from server.core import Server
import os

def accept_request(cls, signal):
    cls.send_data(signal.socket_, open(os.path.join("test", "index.html"), "rb"), file_type=True)

d = Server(accept_request)
d.bind_server()
d.start()