import datetime
import hashlib
import re
import os
from adamantite.engine.tools.default_settings import STATUS_CODE_ABREVIATIONS



class HttpResponse:


    def __init__(self):
        self.__header_ = {}
        self.__body = ""
        self.__abreviation = ""
        self.__protocol_ = ""
        self.__status_code = ""
    
    def set_response_line(self, status_code, protocol_type):
        self.__status_code = status_code
        self.__protocol_ = protocol_type
        self.__abreviation = STATUS_CODE_ABREVIATIONS[status_code]

        # print('asdasdas = ', self.__status_code, self.__protocol_, self.__abreviation, "\n\n\n\n")


    def set_content(self, content):
        self.__body = content
        # print(self.__body)
        

    def modify_response_line(self, key, value):
        if key == "protocol":
            self.__protocol_ = value

        elif key == "status_code":
            self.__status_code = value
            self.__abreviation = STATUS_CODE_ABREVIATIONS[str(value)]


    def __str__(self):
        return self.get_response

    def __repr__(self):
        return f"<ResponseObject at {hex(id(self))}>"


    def get_header_value(self, name):
        """
        Return attribute value of response header from given name
        """

        if not name in self.__header_:
            return

        return self.__header_[name]


    def remove_response_header(self, *params):
        for param in params:
            if param in self.__header_:
                del self.__header_[param]


    def add_response_header(self, params):
        """
        :params must be in dict type

        also can be use to change the header field value
        """
        for param in params:
            self.__header_[param] = str(params[param])

    
    @property
    def get_header(self):
        return self.__header_


    @property
    def construct_headers(self):
        """
        called when get_response called
        """
        header = ""

        for field in self.__header_:
            header += f"{field}: {self.__header_[field]}\n"

        return header


    @property
    def get_response(self):
        if not all((self.__protocol_, self.__status_code, self.__abreviation)):
            raise Exception("Cannot construct response with empty or invalid response line, check again if you set protocol, status_code, abreviation, properly")

        return f"{self.__protocol_} {self.__status_code} {self.__abreviation}\n{self.construct_headers}\n{self.__body}"




class HttpRequest:
    def __init__(self, header_):        
        self.header = header_

        self.request_line = self.header.split("\n")[0]
        self.request_headers = self.header.split("\n")[1:-2]
        self.request_body = self.header.split("\n")[-1]
        self.header_fields = {}
        self.get_method_pattern = re.compile(r"[\?]?\w*=\w*[\&]?")


        for field in self.request_headers:
            key, value = field.strip("\r").split(":", maxsplit=1)
            self.header_fields[key] = value.strip()

    def __str__(self):
        return f"<RequestObject at {hex(id(self))}>"

    def __repr__(self):
        return  f"<RequestObject at {hex(id(self))}>"


    @property
    def is_valid(self):
        if not self.header:
            return False

        return all((self.request_line ,self.request_headers))


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
            key, val = None, None

            for match in self.get_method_pattern.finditer(get_data):
                start_, end_ = match.span()

                if get_data[start_] == "?":
                    start_ += 1

                if get_data[end_-1] == "&":
                    end_ -= 1


                key, val = get_data[start_:end_].split("=")

                key = key.replace("%26", "&")
                val = val.replace("%26", "&")

                data[key] = val


        return data


