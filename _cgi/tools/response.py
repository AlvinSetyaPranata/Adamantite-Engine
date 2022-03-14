from adamantite._cgi.core.managers import Default_Header
from adamantite._cgi.handlers.template import template



class Response_Content:

    @classmethod
    def render(self, request, response, template_path, settings):
        # content, status_code, file_handler, etag = template.Handle().get_template(template_path)

        return Default_Header(settings).default_200(request, response, template_path)


