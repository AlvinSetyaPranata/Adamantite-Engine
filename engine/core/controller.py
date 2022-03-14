from adamantite.engine.handlers.threads import Stoppable_Thread
from adamantite.engine.handlers.services import base_analyze


class Controller:
    def __init__(self, used_settings, callback, read_sockets, report_to):

        self.threads = []
        self.read_sockets = read_sockets
        self.report_to = report_to
        self.used_settings = used_settings
        self.__max_thread = used_settings["MAX_THREAD_ALLOWED"]
        self.request_pools = []
        self.callback = callback


        if not callable(self.callback):
            raise TypeError(f"callback function is not callable")


    def __del__(self):
        for active_thread in self.threads:
            active_thread.stop()


    def report(self, content, level):

        if self.report_to == print:
            self.report_to(content)

        else:
            self.report_to(content, level)


    def create_executor(self, *args):
        """
        Create new thread that run request pool executor
        """

        if self.__max_thread == "EACH":
            pass

        elif len(self.threads) > int(self.__max_thread):
            return

        thread_ = Stoppable_Thread(target=self.pool_executor, args=args)
        self.threads.append(thread_)
        thread_.start()


    def pool_executor(self, request_object, c_sock, http_response):
        self.request_pools.append(request_object)

        if not self.request_pools:
            return

        request_object = self.request_pools.pop(0)
        response_object, connection_stat = base_analyze(self.used_settings, request_object, http_response)


        # set attribute to the controller
        controller = Request_Controller()
        setattr(controller, "client_socket", c_sock)
        setattr(controller, "close", lambda: self.dispatch(self.client_socket))


        if not connection_stat and c_sock in self.read_sockets:
            self.dispatch(c_sock)
            return


        self.callback(request_object ,response_object, controller)


class Request_Controller:
    client_socket = None    # just for abstract


    def send(self, header_content, fileIO_content=None):
        self.client_socket.send(header_content)

        if fileIO_content:
            self.client_socket.sendfile(fileIO_content)
            if not fileIO_content.closed:
                fileIO_content.close()
