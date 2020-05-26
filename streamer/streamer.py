import usocket
import ustruct
import ujson
import utime

from utils.circular_buffer import CircularBuffer


class MulticastStreamer:
    def __init__(self, multicast_group=('224.3.29.71', 65027), hist=0):
        self.send = self._send
        if hist > 0:
            # resend the last values
            self._hist = CircularBuffer(hist)
            self.send = self._send_with_hist
        # keep track of the number of messages send
        self._count = 0
        # save the multicast multicast group to send data
        self._multicast_group = multicast_group
        # Create the datagram socket
        self._socket = usocket.socket(usocket.AF_INET, usocket.SOCK_DGRAM)

    def _send(self, data):
        msg = {'seq': self._count,
               'time': utime.ticks_us(),
               'data': data}

        self._socket.sendto(ujson.dumps(msg), self._multicast_group)
        self._count += 1

    def _send_with_hist(self, data):
        msg = {'seq': self._count,
               'time': utime.ticks_us(),
               'data': data}
        for i, d in enumerate(self._hist):
            msg['data_t-'+str(i)] = d

        self._socket.sendto(ujson.dumps(msg), self._multicast_group)
        self._count += 1
        self._hist.put(data)


def test(h=0):
    ms = MulticastStreamer(hist = h)
    count = 0
    while(True):
        ms.send({'count': count, 'teta': 'mishuevos'})
        count += 1
