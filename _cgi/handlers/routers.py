# from _cgi.tools.url import Url_Handler
from adamantite._cgi.handlers.template.template import Handle as t_handle
# from adamantite._cgi.core import View_Handler
from adamantite._cgi.core.managers import Default_Header
from adamantite._cgi.handlers.exceptions import Invalid_View
import os



class Router:
    def __init__(self,routes, static_url=None, static_root=None):
        self._paths = {}
        self.temp_ = t_handle
        self.routes = routes
        self.static_url = static_url
        self.static_root = static_root
        self.default_header = None     # it will be override when class initialized by App

        for route in routes:
            self.add_path(*route)



    def add_path(self, path, view):
        if view == None:
            raise Invalid_View(f"{view} is not valid view, use View_Handler")

        if not path in self._paths:
            self._paths[path] = view


    def callback(self, request, response_object, controller):     # all incoming socket from server will goes here
        req_path = request.get_path
        
        
        if self.static_url in req_path or "." in os.path.basename(req_path):
            response, fileio = self.default_header.get_static(request, response_object, self.static_root)

            controller.send(response, fileIO_content=fileio)
            return


        if not req_path in self._paths:
            response, fileio = self.default_header.default_404(request, response_object)
            controller.send(response.get_response.encode(), fileIO_content=fileio)
            return

        else:
            view_target = self._paths[req_path]
            http_method = request.get_method


            if http_method == "GET":
                response, fileio = view_target.get(request, response_object)

            elif http_method == "POST":
                response, fileio = view_target.post(request, response_object)


            if not response:
                raise TypeError("Expected to be response object")


            controller.send(response, fileIO_content=fileio)
