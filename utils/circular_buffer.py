class CircularBuffer:
    def __init__(self, max_size):
        self._max_size = max_size
        self._buffer = ['']*self._max_size
        self._index = 0

    def put(self, item):
        try:
            self._buffer[self._index] = item
            self._index += 1
        except:
            self._buffer[0] = item
            self._index = 1

    def __iter__(self):
        temp = self._buffer[self._index:]+self._buffer[:self._index]
        temp.reverse()
        return iter(temp)
