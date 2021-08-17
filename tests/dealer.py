import time
from threading import Thread

import zmq


def dealer():
    context = zmq.Context.instance()
    dealer_socket = context.socket(zmq.DEALER)
    dealer_socket.setsockopt(zmq.IDENTITY, bytes("dealer", encoding="utf-8"))
    dealer_socket.connect("tcp://172.16.165.136:61616")

    while True:
        request = dealer_socket.recv()
        print(request)

        dealer_socket.send_multipart([b"", b"this is test message"])


Thread(target=dealer).start()
