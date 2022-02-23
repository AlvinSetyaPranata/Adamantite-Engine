class Request_Abstract:
    def __init__(self, header, socket_):
        self.header = header
        self.splited_header = header.split("\n")
        self.socket_ = socket_

    @property
    def get_protocol(self):
        return self.splited_header[0].split()[-1]

    @property
    def get_method(self):
        return self.splited_header[0].split()[0]

    @property
    def get_path(self):
        return self.splited_header[0].split()[1]

    @property
    def get_method_data(self):
        pass

    