import hashlib as _hash

import os

from adamantite._cgi.handlers.exceptions import Template_Not_Found
from adamantite._cgi import BUILTIN_FILE_PATH


MD5 = _hash.md5
SHA1 = _hash.sha1
SHA224 = _hash.sha224
SHA256 = _hash.sha256
SHA384 = _hash.sha384


class Handle:

    @classmethod
    def set_etag(self, data,  method=MD5):
        if type(data) is bytes:
            return method(data).hexdigest()

        else:
            return method(data.encode()).hexdigest()
        


    def get_template(self, file_path):
        """
        Return template content, status code, fileIO, and etag
        """
        

        if not os.path.isfile(file_path):
            # with open(os.path.join(BUILTIN_FILE_PATH, "page_404.html"), "r") as template:
            #     return template.read().strip(), "404", open(os.path.join(BUILTIN_FILE_PATH, "page_404.html"), "rb")
            return self.get_builtin("page_404.html")



        with open(file_path, "r") as f:
            content = f.read()

            return content.strip(), "200", open(file_path, "rb"), self.set_etag(content)
            

    def get_static(self, file_path):
        if not os.path.isfile(file_path):
            content, _, file_h, etag = self.get_builtin("page_404.html")
            return content, "404", file_h, etag


        with open(file_path, "r") as f:
            content = f.read()

            return content.strip(), "200", open(file_path, "rb"), self.set_etag(content)


    def get_builtin(self, fname):
        file_path = os.path.join(BUILTIN_FILE_PATH, fname)


        if not os.path.isfile(file_path):
            raise Template_Not_Found(f"Cannot find template with name {fname}")


        with open(file_path, "r") as f:
            content = f.read()

            return content.strip(), "200", open(file_path, "rb"), self.set_etag(content)
        