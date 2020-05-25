import network

# https://docs.micropython.org/en/latest/library/network.WLAN.html

class Station:
    def __init__(self):
        self._conn = network.WLAN(network.STA_IF)

    def activate(self):
        self._conn.active(True)

    def deactivate(self):
        self._conn.active(False)

    def connect(self, essid, password):
        self._conn.active(True)
        self._conn.connect(essid, password)
        while not self._conn.isconnected():
            pass

    def disconnect(self):
        self._conn.disconnect()

    def get_connection(self):
        return self._conn

    def set_ip(self, ip):
        _ip = list(self._conn.ifconfig())
        _ip[0] = ip
        self._conn.ifconfig(tuple(_ip))


class AccessPoint:
    def __init__(self):
        self._conn = network.WLAN(network.AP_IF)

    def activate(self):
        self._conn.active(True)

    def deactivate(self):
        self._conn.active(False)

    def connect(self, essid, password):
        self._conn.active(True)
        self._conn.config(essid=essid, password=password)
        while not self._conn.isconnected():
            pass

    def disconnect(self):
        self._conn.disconnect()

    def get_connection(self):
        return self._conn
