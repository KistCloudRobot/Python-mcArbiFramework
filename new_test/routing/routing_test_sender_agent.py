from arbi_agent.agent.arbi_agent import ArbiAgent
from arbi_agent.agent import arbi_agent_excutor


class RoutingTestAgentSender(ArbiAgent):
    def on_start(self):
        self.send("agent://www.arbi.com/TestReceiver/receiverAgent", "(testData)")


if __name__ == '__main__':
    agent = RoutingTestAgentSender()
    arbi_agent_excutor.excute("tcp://127.0.0.1:61316", "agent://www.arbi.com/TestSender/senderAgent",
                              agent, 2)
    input()
