import connections.wifi
import connections.http_handler
import database.btreedb


def connect_known(station, known_networks_db, timeout):
    print('Searching for known networks...')
    station.activate()
    available_networks = station.scan()

    for ssid, bssid, channel, RSSI, authmode, hidden in available_networks:
        if ssid in known_networks_db:
            print('Trying to connect to %s...' % ssid)
            if station.connect(ssid, known_networks_db[ssid], timeout):
                print('Connected to %s with ip %s.' % (ssid, station.ifconfig()[0]))
                return True
    return False


def connect(wlan_station, path_networks_db='/data/networks.db', timeout=5):

    networks_db = database.btreedb.BtreeDB(path_networks_db)

    if not connect_known(wlan_station, networks_db, timeout):
        print('No known network found.')
        # there is no known network
        # create an access point
        print('Creating access point.')
        access_point = connections.wifi.AccessPoint()
        # access_point.set_ip('192.168.0.1')
        ssid = 'esp32 - ' + access_point.ifconfig()[0] + ':65000'
        access_point.connect(ssid, '')
        print('Access point created with ssid: "%s"' % ssid)
        print('Please, connect to the access point and use a webbroser to access "%s:65000".' % access_point.ifconfig()[0])

        # prepare to serve http requests
        http_handler = connections.http_handler.Server((access_point.ifconfig()[0], 65000))

        # loop geting credentials and trying to connect
        while not wlan_station.isconnected():
            # not known network found, serve a webpage to introduce new credentials
            new_ssid, new_password = http_handler.get_new_credentials()
            wlan_station.connect(new_ssid, new_password, timeout)

        # we are connected to the new network, sabe it in the database
        print('Saving the new network into the database.')
        networks_db[new_ssid] = new_password
        networks_db.flush()
        networks_db.close()

        # deactivate the access point
        print('Deactivating access point...')
        access_point.deactivate()

    return wlan_station
