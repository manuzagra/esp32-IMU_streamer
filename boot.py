# This file is executed on every boot (including wake-boot from deepsleep)
#import esp
#esp.osdebug(None)
#import webrepl
#webrepl.start()

import utils
import connections

wifi_station = connections.wifi.Station()
wifi_station.connect('Cebolleta', 'tiguer32')
wifi_station.set_ip('192.168.0.40')


import utils.uftpd
