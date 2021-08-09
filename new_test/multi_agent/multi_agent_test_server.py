import time

from arbi_agent.framework.arbi_framework_server import ArbiFrameworkServer


if __name__ == '__main__':
    server = ArbiFrameworkServer("TestServer", 0)
    broker_url = "tcp://127.0.0.1:61616"
    server.start(broker_url)
    while True:
        time.sleep(1)
