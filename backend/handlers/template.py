import os

class Handle:
    def get_template(self, file_path):
        if os.path.isfile(file_path):
            return "" "404"

        with open(file_path, "r") as f:
            return f.read(), "200"

    def get_assets(self):
        pass
            