import streamer


def test():
    ms = streamer.MulticastStreamer()
    count = 0
    while(True):
    ms.send({'count': count, 'another_field': 'content of the other field'})
    count += 1
