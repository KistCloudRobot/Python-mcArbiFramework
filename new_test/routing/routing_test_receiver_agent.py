from arbi_agent.agent.arbi_agent import ArbiAgent
from arbi_agent.agent import arbi_agent_excutor


class RoutingTestAgentReceiver(ArbiAgent):
    def on_data(self, sender: str, data: str):
        print("received! " + data + " " + sender)


if __name__ == '__main__':
    agent = RoutingTestAgentReceiver()
    arbi_agent_excutor.excute("tcp://127.0.0.1:61116", "agent://www.arbi.com/TestReceiver/receiverAgent",
                              agent, 2)
    input()
