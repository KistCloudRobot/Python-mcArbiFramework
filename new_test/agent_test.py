from arbi_agent.agent.arbi_agent import ArbiAgent
from arbi_agent.agent import arbi_agent_executor
from arbi_agent.configuration import BrokerType
from time import sleep

class TestAgent(ArbiAgent):
    def __init__(self):
        super().__init__()

    def on_data(self, sender: str, data: str):
        print(self.agent_url + "\t-> receive data : " + data)

    def on_request(self, sender: str, request: str) -> str:
        print(self.agent_url + "\t-> receive request : " + request)
        return "(request ok)"

    def on_query(self, sender: str, query: str) -> str:
        print(self.agent_url + "\t-> receive query : " + query)
        return "(query ok)"


if __name__ == '__main__':
    broker_url = "tcp://127.0.0.1:61116"

    sender_agent = TestAgent()
    sender_agent_name = "agent://www.arbi.com/Local/SenderAgent"
    arbi_agent_executor.execute(broker_url, agent_name=sender_agent_name, agent=sender_agent, broker_type=BrokerType.ZERO_MQ)
    print("sender agent ready")

    receiver_agent = TestAgent()
    receiver_agent_name = "agent://www.arbi.com/Local/ReceiverAgent"
    arbi_agent_executor.execute(broker_url, agent_name=receiver_agent_name, agent=receiver_agent, broker_type=BrokerType.ZERO_MQ)
    print("receiver agent ready")

    print("test start!")

    # agent1 send test message to agent2
    input()
    print(sender_agent_name + " -> send test")
    sender_agent.send(receiver_agent_name, "(test send)")

    input()
    # agent1 request to agent2
    print(sender_agent_name + " -> rquest test")
    response = sender_agent.request(receiver_agent_name, "(test request)")
    print(sender_agent_name + " -> response : " + response)
    sleep(3)

    input()
    # agent1 query to agent2
    print(sender_agent_name + " -> query test")
    response = sender_agent.query(receiver_agent_name, "(test query)")
    print(sender_agent_name + " -> response : " + response)
    sleep(3)

    print("test finished")
    sender_agent.close()
    receiver_agent.close()
