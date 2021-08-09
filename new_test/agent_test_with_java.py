from arbi_agent.agent.arbi_agent import ArbiAgent
from arbi_agent.configuration import BrokerType
from time import sleep
from threading import Condition


class TestAgent(ArbiAgent):
    def __init__(self):
        super().__init__()
        self.lock = Condition()

    def on_data(self, sender, data):
        print("on data : " + data)
        with self.lock:
            self.lock.notify_all()

    def on_request(self, sender, request):
        print("on request : " + request)
        with self.lock:
            self.lock.notify_all()
        print("send response : (test response from python)")
        return "(test response from python)"

    def on_query(self, sender, query):
        print("on query : " + query)
        with self.lock:
            self.lock.notify_all()
        print("send response : (test query response from python)")
        return "(test query response from python)"

    def agent_to_agent_test(self):
        message = "(test send from python)"
        print("send :", message)
        self.send("agent://jam_agent", message)
        sleep(1)
        with self.lock:
            self.lock.wait()
        sleep(1)
        message = "(test request from python)"
        print("request :", message)
        response = self.request("agent://jam_agent", message)
        print("response :", response)
        sleep(1)
        with self.lock:
            self.lock.wait()
        sleep(1)
        message = "(test query from python)"
        print("query :", message)
        response = self.query("agent://jam_agent", message)
        print("response : " + response)
        with self.lock:
            self.lock.wait()
        sleep(1)
        print("test finished")


if __name__ == "__main__":
    agent = TestAgent()
    agent.initialize(agent_url="agent://python_agent", broker_url="tcp://127.0.0.1:61616",
                     broker_type=BrokerType.TYPE_ZERO)

    print("agent ready")

    input()

    print('start')
    agent.agent_to_agent_test()
