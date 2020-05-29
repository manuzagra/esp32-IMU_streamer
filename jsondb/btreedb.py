import btree
import ujson

class DataBase:
    def __init__(self, path=None):
        self._fd = None
        self._db = None
        if path:
            self.open(path)

    def open(self, path):
        try:
            self._fd = open(path, "r+b")
        except OSError:
            self._fd = open(path, "w+b")

        self._db = btree.open(self._fd)

    def close(self):
        self._db.close()
        self._fd.close()

    def flush(self):
        self._db.flush()

    def __setitem__(self, key, val):
        self._db[key] = ujson.dumps(val)

    def __getitem__(self, key):
        return ujson.loads(self._db[key])

    def get(self, key, default=None):
        return ujson.loads(self._db.get(key, default))

    # from here maybe its better to do it in this way:
    # https://stackoverflow.com/questions/13460889/how-to-redirect-all-methods-of-a-contained-class-in-python
    def __deltitem__(self, key):
        self._db.__detitem__(key)

    def __contains__(self, key):
        return self._db.__contains__(key)

    def __iter__(self):
        return self._db.__iter__()

    def keys(self, start_key=None, end_key=None, flags=0):
        return list(self._db.keys(start_key, end_key, flags))

    def values(self, start_key=None, end_key=None, flags=0):
        temp_values = self._db.values(start_key, end_key, flags)
        return [ujson.loads(d) for d in temp_values]

    def items(self, start_key=None, end_key=None, flags=0):
        temp_items = self._db.items(start_key, end_key, flags)
        return [(k, ujson.loads(v)) for k,v in temp_items]
