from ..handlers import template

STATUS_CODE_ABREVIATIONS = {
    "200" : "OK",
    "404" : "Not Found"
}


class Header:
    def __init__(self):
        self.t_handler = template.Handle()

    def default_404(self, request):
        request.add_response_header(
            {
                "Transfer-Encoding" : "chunked",
                "X-Powered-By" : "Adamantite-Framework v0.1"
            }
        )
        
        
        setattr(request, '__status_code', "404")
        setattr(request, '__protocol', request.get_protocol)
        setattr(request, '__abreviation', STATUS_CODE_ABREVIATIONS["404"])
        setattr(request, '__body', self.t_handler.get_builtin("not_found_404.html"))

        return request.construct_header