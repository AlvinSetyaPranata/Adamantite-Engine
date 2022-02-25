from server.core import Server
from ..tools.url import Url_Handler
from .managers import Header



class Setting_Abstract(Server):
    def __init__(self):
        self.resource_dir = ""
        self.ip_ = "127.0.0.1"
        self.port = 5000
        self.view_handler = None

        super().__init__(self.view_handler, self.ip_, self.port)


class View_Abstract(managers.Header):
    """
    Define all your view in here
    """