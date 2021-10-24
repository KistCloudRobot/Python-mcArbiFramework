import uuid
from time import sleep

from arbi_agent.agent.arbi_agent import ArbiAgent
from arbi_agent.agent import arbi_agent_executor


class TestAgent(ArbiAgent):
    def __init__(self):
        super().__init__()

    def on_data(self, sender: str, data: str):
        message = self.get_full_message()
        print("sender\t\t:", message.get_sender())
        print("receiver\t:", message.get_receiver())
        print("conversation id\t:", message.get_conversation_id())
        print("timestamp\t:", message.get_timestamp())


if __name__ == '__main__':
    broker_url = "tcp://127.0.0.1:61616"

    sender_agent = TestAgent()
    sender_agent_name = "agent://www.arbi.com/SenderAgent"
    arbi_agent_executor.excute(broker_url, agent_name=sender_agent_name, agent=sender_agent, broker_type=2)
    print("sender agent ready")

    receiver_agent = TestAgent()
    receiver_agent_name = "agent://www.arbi.com/ReceiverAgent"
    arbi_agent_executor.excute(broker_url, agent_name=receiver_agent_name, agent=receiver_agent, broker_type=2)
    print("receiver agent ready")

    print("test start!")

    sleep(1)
    sender_agent.send(receiver_agent_name, "(testsend 1)")
    sleep(1)

    print("test finished")
    sender_agent.close()
    receiver_agent.close()
