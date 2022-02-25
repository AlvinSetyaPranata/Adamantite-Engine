from ..core.managers import Header


class Url_Handler:
    def check_url(self, url_):
        pass


    def get(self, request, **params):
        idx = 0
        dest = request.get_path

        for param in params:
            if idx > 0:
                dest += "?" + param + "=" + params[param]

            else:
                dest += "&" + param + "=" + params[param]

            idx += 1

        return dest

    def post(self, request, **params):
        idx = 0
        body = ""
        request.add_response_header("Content-Type", "application/x-www-form-urlencoded")    

        for param in params:
            if idx > 0:
                body += "&" + param + "=" + params[param]

            else:
                body += param + "=" + params[param]

            idx += 1

        setattr(request, "__body", body)

        return request