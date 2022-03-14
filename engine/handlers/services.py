import datetime





class Protocol_analyze:

    @classmethod
    def http_1_0(self, request_):
        if not "Connection" in request_.header_fields:
            return 0


        if request_.header_fields["Connection"] == "keep-alive":
            return 1

        else:
            return 0


    @classmethod
    def http_1_1(self, request_):
        if request_.header_fields["Connection"] == "keep-alive":
            return 1

        else:
            return 0




def base_analyze(settings, request_, response_object):
    proto_cls = Protocol_analyze
    response_fields = {}


    # set the response field
    response_fields["Date"] = datetime.datetime.utcnow().strftime("%a, %d %B %Y %H:%M:%S GMT")
    response_fields["Server"] = "AdamantiteEngine v0.1 BETA"
    response_fields["Host"] = settings["HOST"]
    response_fields["Cache-Control"] = "no-cache"
    

    response_object.add_response_header(response_fields)
    response_object.set_response_line("200", request_.get_protocol)     # set the default value

    if request_.get_protocol == "HTTP/1.1":
        connection_stat = proto_cls.http_1_1(request_)

    else:
        connection_stat = proto_cls.http_1_0(request_)


    return response_object, connection_stat


