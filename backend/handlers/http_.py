import datetime
import hashlib
import re



STATUS_CODE_ABREVIATIONS = {
    "200" : "OK",
    "404" : "Not Found"
}


class HttpResponse:
    # Meta Data

    __abreviation = ""
    __protocol_ = ""
    __status_code = ""

    def __init__(self):
        self.__header_ = {
            "Date" : datetime.datetime.utcnow().strftime("%a, %d %B %Y, %H:%M:%S GMT"),
            "Server" : "Adamantite-Engine v0.1 Beta",
        }
        
        self.__body = ""

    
    def set_response_line(self, status_code, protocol_type):
        self.__status_code = status_code
        self.__protocol_ = protocol_type
        self.__abreviation = STATUS_CODE_ABREVIATIONS[str(status_code)]


    def __str__(self):
        return f"<ResponseObject at {hex(id(self))}>"


    def get_header_value(self, name):
        """
        Return attribute value of response header from given name
        """

        if not name in self.__header_:
            return

        return self.__header_[name]


    def add_response_header(self, params):
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

        return f"{self.__protocol_} {self.__status_code} {self.__abreviation}\n{self.construct_headers}\n\n{self.__body}"


    @classmethod
    def add_etag(self, content, hashmethod=hashlib.sha256):
        if not type(content) is bytes:
            content = content.encode()

        return {"ETag" : hashmethod(content).hexdigest()}


class HttpRequest:
    def __init__(self, header, socket_):
        super().__init__()
        
        self.header = header
        self.request_line = self.header.split("\n")[0]
        self.request_headers = self.header.split("\n")[1:-2]
        self.request_body = self.header.split("\n")[-1]

        self.header_fields = {}

        self.get_method_pattern = re.compile(r"[\?]?\w*=\w*[\&]?")
        
        self.socket_ = socket_
        self.response_object = HttpResponse()

        for field in self.request_headers:
            key, value = field.strip("\r").split(":", maxsplit=1)
            self.header_fields[key] = value

    def __str__(self):
        return f"<RequestObject at {id(self)}>"


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


            
if __name__ == "__main__":
    d = HttpRequest()