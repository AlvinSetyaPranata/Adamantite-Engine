from threading import Thread, Event


class Stoppable_Thread(Thread):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__stop_flag = Event()

    def stop(self):
        self.__stop_flag.set()

    def is_stopped(self):
        return self.__stop_flag.is_set()