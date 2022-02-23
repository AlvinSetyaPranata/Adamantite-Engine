class Base_Abstract:
    def route(self, path, dest):
        return (path, dest)


class Abstract(Base_Abstract):
    def __init__(self):
        self.home = self.route("/", "")
