import datetime
import re

class Response:
    def __init__(self):
        self.__header_ = {
            "Date" : datetime.datetime.utcnow().strftime("%a, %d %B %Y, %H:%M:%S GMT"),
            "Server" : "Adamantite Engine v0.1 Beta",
            "Content-Encoding" : "gzip",
            "Connection" : "closed",
        }

    def add(self, param_name, value):
        self.__header_[param_name] = value

    @property
    def get_header(self):
        return self.__header_



class Request(Response):
    def __init__(self, header, socket_):
        super().__init__()
        
        self.header = header
        self.request_line = self.header.split("\n")[0]
        self.request_headers = self.header.split("\n")[1]
        self.request_body = self.header.split("\n")[-1]

        self.get_method_pattern = re.compile(r"[\?]?\w*=\w*[\&]?")
        self.post_method_pattern = re.compile(r"")
        
        self.socket_ = socket_

        # print(self.request_body)

    @property
    def get_protocol(self):
        return self.request_line.split()[-1]

    @property
    def get_method(self):
        return self.request_line.split()[0]

    @property
    def get_path(self):
        return self.request_line.split()[1]

    @property
    def get_method_data(self):
        data = {}

        if self.get_method == "POST":
            for x in self.request_body.split("&"):
                key, val = x.split("=")

                key = key.replace("%26", "&")
                val = val.replace("%26", "&")

                data[key] = val

        elif self.get_method == "GET":
            get_data = self.request_line.split()[1]

            for match in self.get_method_pattern.finditer():
                start_, end_ = match.span()

                if start_ == "?":
                    start_ += 1

                if end_-1 == "&":
                    end_ -= 1

                key = key.replace("%26", "&")
                val = val.replace("%26", "&")

                data[key] = val


        return data


            


    