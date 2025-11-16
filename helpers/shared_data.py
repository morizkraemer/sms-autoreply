import threading

class SharedData:
    def __init__(self):
        self._lock = threading.Lock()
        self._reply_message = "hey there, nice to meet you"

    def get_reply_message(self):
        with self._lock:
            return self._reply_message

    def set_reply_message(self, new_message):
        with self._lock:
            self._reply_message = new_message


shared_data = SharedData()
