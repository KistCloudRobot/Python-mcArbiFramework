from time import sleep

from arbi_agent.agent import arbi_agent_excutor
from new_test.agent_test import TestAgent


if __name__ == '__main__':
    broker_url = "tcp://127.0.0.1:61616"

    receiver_agent = TestAgent()
    sender_agent_name = "agent://www.arbi.com/SenderAgent"
    receiver_agent_name = "agent://www.arbi.com/ReceiverAgent"
    arbi_agent_excutor.excute(broker_url, agent_name=receiver_agent_name, agent=receiver_agent, broker_type=2)
    print("receiver agent ready")

    while True:
        sleep(1)
