from backend.tools.url import Url_Handler
from .template import Handle as t_handle
from server.core import Server
from server.core.handlers import Response
from ..core import managers


class Base_Abstract(managers.Header, Url_Handler):
    def __init__(self):
        self.__template_handler = t_handle()

    def route(self, path, dest):
        return (path, dest)

    def get_static(self, file_name):
        content, status_code = self.__template_handler.get_template(file_name)

        if status_code == "404":
            return self.default_404()


class Router(Base_Abstract):
    """
    Define all your routes pattern in __init__ method
    
    e.g:

    self.home = self.route('/', self.get_static(page_name))
    self.login = self.route('/), self.get_static(page_name))
    
    """
    def __init__(self):
        super().__init__()
