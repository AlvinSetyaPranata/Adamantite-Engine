import os


BUILTIN_FILE_PATH = os.path.join(os.path.dirname(__file__), "builtin_pages")

class Handle:

    def get_template(self, file_path):
        """
        Return template content and status code
        """
        if not os.path.isfile(file_path):
            return None, "404"

        with open(file_path, "r") as f:
            return f.read(), "200"

    def get_assets(self):
        pass
            
    def get_builtin(self, fname):
        f_path = os.path.join(BUILTIN_FILE_PATH, fname)

        if not os.path.isfile(f_path):
            return ""

        f_open = open(f_path, "r")
        content = f_open.read()
        f_open.close()

        return content
        