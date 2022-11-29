from arbi_agent.agent.arbi_agent import ArbiAgent
from arbi_agent.agent import arbi_agent_executor
from arbi_agent.configuration import BrokerType
from time import sleep


class TestAgent(ArbiAgent):
    def __init__(self):
        super().__init__()

    def on_data(self, sender: str, data: str):
        print(self.agent_uri + "\t-> receive data : " + data)

    def on_request(self, sender: str, request: str) -> str:
        print(self.agent_uri + "\t-> receive request : " + request)
        return "(request ok)"

    def on_query(self, sender: str, query: str) -> str:
        print(self.agent_uri + "\t-> receive query : " + query)
        return "(query ok)"


if __name__ == '__main__':
    test_agent = TestAgent()
    test_agent_name = "agent://www.arbi.com/TestAgent"
    arbi_agent_executor.execute(broker_host="127.0.0.1", broker_port=61616, agent_name=test_agent_name, agent=test_agent, broker_type=BrokerType.ACTIVE_MQ)

    print("test start!")

    # agent1 send test message to agent2
    sleep(1)
    test_agent.send(test_agent_name, "(test \"asdf\")")
    sleep(5)
