# from _cgi.tools.url import Url_Handler
# from _cgi.handlers.template.parser import Html_String
# from _cgi.handlers.template.template import Handle as template_handler
# from _cgi.core.managers import Default_Header
from adamantite._cgi.core.managers import Default_Header
from adamantite._cgi.handlers.routers import Router
from adamantite._cgi.tools import get_locals
from adamantite._cgi.tools.report import Reporter
from adamantite.engine.core import Server




class App:
    def __init__(self, settings, router):
        self.__reporter = Reporter()

        setattr(router, "default_header", Default_Header(settings))

        self.__server = Server(settings, router.callback, report=self.__reporter.report)



    def runserver(self):
        self.__server.bind_server()
        self.__server.start()



class View_Handler:

    def get(self, request, *args, **kwarags):
        """
        Override this method to handle GET request
        """


    def post(self, request, *args, **kwargs):
        """
        Override this method to handle POST request
        """





