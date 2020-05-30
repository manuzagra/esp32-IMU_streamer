import connetions.wifi
import database.btreedb
import connetions.http_handler




class WiFiManager:
    def __init__(self, networks_db='/data/networks.db'):
        self._station = connetions.wifi.Station()

        self._networks_db = database.btreedb.BtreeDB(networks_db)

    def connect_known(self):
        available_networks = self._station.scan()

        for ssid, bssid, channel, RSSI, authmode, hidden in available_networks:
            if ssid in self._networks_db and self._station.connect(ssid, self._networks_db[ssid], timeout=5):
                return True
        return False

    def auto_connect(self, timeout=5):

        if self.connect_known():
            return self._station

        access_point = connetions.wifi.AccessPoint()
        access_point.connect('esp32', '')
        while not self._station.isconnected():
            # not known network found, serve a webpage to introduce new credentials
            new_ssid, new_password = self.get_new_credentials()
            self._station.connect(new_ssid, new_password, timeout)

        # we are connected to the new network
        self._networks_db[new_ssid] = new_password
        self._networks_db.flush()
        self._networks_db.close()
        return self._station


    def get_new_credentials(self):
        print('serving a webpage')

        return 'ssid_', 'password'
