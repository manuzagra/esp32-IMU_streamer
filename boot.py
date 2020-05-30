# This file is executed on every boot (including wake-boot from deepsleep)
#import esp
#esp.osdebug(None)
#import webrepl
#webrepl.start()


import connections

# Create an interface and connect it to the local network
wifi_station = connections.wifi.Station()
wifi_station = connections.manager.connect(wifi_station)
wifi_station.set_ip('192.168.0.40')

import utils
import utils.uftpd


