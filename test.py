import time
import sys
import stomp


class Listener(stomp.ConnectionListener):
    def on_message(self, frame):
        print('received a message :', frame)
        print(frame.body)


hosts = [('127.0.0.1', 61616)]
conn = stomp.Connection(host_and_ports=hosts)
conn.set_listener('', Listener())
conn.connect(wait=True)
conn.subscribe(destination='queue', id='asdf')
conn.send(body="hello", destination='queue')
conn.send(body="hello java", destination='java')
time.sleep(10)
conn.disconnect()
