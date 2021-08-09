
from arbi_agent.agent import arbi_agent_excutor
from arbi_agent.agent.arbi_agent import ArbiAgent
from arbi_agent.framework.arbi_framework_server import ArbiFrameworkServer
from arbi_agent.configuration import BrokerType
import time


class TestMultiAgent(ArbiAgent):
    def on_data(self, sender: str, data: str):
        print("received!")
        print("\tdata\t\t:", data)
        print("\tsender\t\t:", sender)
        print()


if __name__ == '__main__':
    num = input("enter agent num : ")
    if len(num) == 0 or len(num) > 3:
        raise Exception("please enter nmber range 0 to 99")
    else:
        if len(num) == 1:
            num = "0" + num
        broker_name = "TestRouter" + num
        broker = ArbiFrameworkServer(broker_name, 2)
        broker_url = "tcp://127.0.0.1:611" + num
        server_url = "tcp://127.0.0.1:61616"
        broker.start(broker_url, server_url)
        agent = TestMultiAgent()
        agent_url = "tcp://127.0.0.1:613" + num
        agent_name = "agent://www.arbi.com/" + broker_name + "/testMultiAgent" + num
        arbi_agent_excutor.excute(broker_url, agent_name,
                                  agent, 2)
        while True:
            receiver_num = input()
            if len(receiver_num) == 0 or len(receiver_num) > 3:
                print("please enter nmber range 0 to 99")
            else:
                if len(receiver_num) == 1:
                    receiver_num = "0" + receiver_num
                receiver_broker_name = "TestRouter" + receiver_num
                receiver_agent_name = "agent://www.arbi.com/" + receiver_broker_name + "/testMultiAgent" + receiver_num
                message = "(test " + num + ")"
                agent.send(receiver_agent_name, message)

