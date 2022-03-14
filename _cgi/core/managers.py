from adamantite._cgi.handlers.template.template import Handle as t_handle
from adamantite.engine.tools.compressions_lib import gzip_compress, lzma_compress, brotli_compress, deflate_compress
from adamantite._cgi.handlers.template import temp_file
from sys import version_info
import os


VERSION = f"Python {version_info.major}.{version_info.minor}.{version_info.micro}"



class Default_Header:
    def __init__(self, settings):
        self.transfer_encoding = settings["COMPRESSION_PRIORITY"]
        self.template_handler = t_handle()


    def _compress_file(self, request_, response_, fileio):
        _used_compression_method = ""
        _content = fileio.read()
        _temp_file = temp_file.create_tempfile()
        _compressed_data = None
        
        

        for comp_ in self.transfer_encoding:
            for acc_ in request_.header_fields["Accept-Encoding"].split():

                if acc_.strip() == comp_:
                    _used_compression_method =  comp_
                    break

            if _used_compression_method:
                break


        if _used_compression_method == "br":
            _compressed_data = brotli_compress(_content, _temp_file)

        elif _used_compression_method == "gzip":
            _compressed_data = gzip_compress(_content, _temp_file)

        elif _used_compression_method == "deflate":
            _compressed_data = deflate_compress(_content, _temp_file)


        response_.add_response_header({"Transfer-Encoding" : _used_compression_method})
        
        return response_.get_response.encode(), _compressed_data


    def get_static(self, request, response, static_root):

        content, status_code, fileio, etag = self.template_handler.get_static(request.get_path.split("/static/")[-1])

        response.add_response_header({"X-Powered-By" : VERSION})
        response.add_response_header({"Content-Disposition" : f"inline; filename=\"{os.path.basename(request.get_path)}\""})
        response.add_response_header({"Content-Length" : str(len(content))})
        response.add_response_header({"ETag" : etag})
        response.set_content(content)


        if status_code == "404":
            response, fileio = self.default_404(request, response)
            return response.get_response.encode(), fileio


        response.modify_response_line("status_code", status_code)
        
        return self._compress_file(request, response, fileio)



    def default_404(self, request_, response):

        content, status_code, fileio, etag = self.template_handler.get_builtin("page_404.html")

        response.add_response_header(
            {
                "Content-Length" : str(len(content)),
                "X-Powered-By" : VERSION,
                "ETag" : etag
            }
        )


        response.modify_response_line("status_code", status_code)

        response.set_content(content)

        return self._compress_file(request_, response,fileio)


    def default_200(self, request, response, template):
        content, status_code, fileio, etag = self.template_handler.get_template(template)

        if status_code == "404":
            return self.default_404(request, response)


        response.add_response_header(
            {
                "Content-Length" : str(len(content)),
                "X-Powered-By" : VERSION,
                "ETag" : etag
            }
        )
        response.modify_response_line("status_code", status_code)
        response.set_content(content)

        return self._compress_file(request, response, fileio)
