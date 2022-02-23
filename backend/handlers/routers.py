from .template import Handle as t_handle

class Base_Abstract:
    def __init__(self):
        self.__template_handler = t_handle
    
    def route(self, path, dest):
        return (path, dest)

    def get_resource(self, file_name):
        pass


class Abstract(Base_Abstract):
    """
    Define all your routes pattern in __init__ method
    
    e.g:

    self.home = self.route('/', self.get_resource(''))
    """
