import btree
import ujson

class BtreeDB:
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

    def __setitem__(self, key, value):
        self._db[ujson.dumps(key)] = ujson.dumps(value)

    def put(self, key, value):
        self._db[ujson.dumps(key)] = ujson.dumps(value)

    def __getitem__(self, key):
        return ujson.loads(self._db[ujson.dumps(key)])

    def get(self, key, default=None):
        return ujson.loads(self._db.get(ujson.dumps(key), default))

    # from here maybe its better to do it in this way:
    # https://stackoverflow.com/questions/13460889/how-to-redirect-all-methods-of-a-contained-class-in-python
    def __delitem__(self, key):
        del self._db[key]

    def __contains__(self, key):
        return ujson.dumps(key) in self._db

    def __iter__(self):
        return iter(self._db)

    def keys(self, start_key=None, end_key=None, flags=0):
        return [ujson.loads(k) for k in self._db.keys(start_key, end_key, flags)]

    def values(self, start_key=None, end_key=None, flags=0):
        return [ujson.loads(v) for v in self._db.values(start_key, end_key, flags)]

    def items(self, start_key=None, end_key=None, flags=0):
        return [(ujson.loads(k), ujson.loads(v)) for k,v in self._db.items(start_key, end_key, flags)]
