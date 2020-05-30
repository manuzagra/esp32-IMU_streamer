import network
import utime

# https://docs.micropython.org/en/latest/library/network.WLAN.html

class Station:
    def __init__(self):
        self._wlan = network.WLAN(network.STA_IF)

    def activate(self):
        self._wlan.active(True)

    def deactivate(self):
        self._wlan.active(False)

    def connect(self, essid, password, timeout=0):
        self._wlan.active(True)
        self._wlan.connect(essid, password)
        for t in range(timeout):
            utime.sleep(1)
            if self._wlan.isconnected():
                return True
        return False

    def disconnect(self):
        self._wlan.disconnect()

    def get_wlanection(self):
        return self._wlan

    def set_ip(self, ip):
        _ip = list(self._wlan.ifconfig())
        _ip[0] = ip
        self._wlan.ifconfig(tuple(_ip))

    def scan(self):
        return self._wlan.scan()


class AccessPoint:
    def __init__(self):
        self._wlan = network.WLAN(network.AP_IF)

    def activate(self):
        self._wlan.active(True)

    def deactivate(self):
        self._wlan.active(False)

    def connect(self, essid, password):
        self._wlan.active(True)
        self._wlan.config(essid=essid, password=password)
        while not self._wlan.isconnected():
            pass
        return True

    def disconnect(self):
        self._wlan.disconnect()

    def get_wlanection(self):
        return self._wlan
