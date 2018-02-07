from threading import Lock

PORT = 9999

END_FLAG = 255
FRAME_LENGTH = 2


class MoveCmd:
    def __init__(self):
        self._lock = Lock()
        self._right = None
        self._left = None

    def write(self, right, left):
        print('Call ' + right + ' ' + left)
        with self._lock:
            self._right = right
            self._left = left

    def read(self):
        with self._lock:
            return self._right, self._left


