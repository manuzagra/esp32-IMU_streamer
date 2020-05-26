import usocket
import ustruct
import ujson
import utime


class MulticastStreamer:
    def __init__(self, multicast_group=('224.3.29.71', 65027)):
        # keep track of the number of messages send
        self._count = 0
        # save the multicast multicast group to send data
        self._multicast_group = multicast_group
        # Create the datagram socket
        self._socket = usocket.socket(usocket.AF_INET, usocket.SOCK_DGRAM)

    def send(self, data):
        msg = {'seq': self._count,
               'time': utime.ticks_us(),
               'data': data}

        self._socket.sendto(ujson.dumps(msg), self._multicast_group)
        self._count += 1


def test():
    ms = MulticastStreamer()
    count = 0
    while(True):
        ms.send({'count': count, 'teta': 'mishuevos'})
        count += 1
