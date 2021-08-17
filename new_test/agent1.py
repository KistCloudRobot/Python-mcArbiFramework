from time import sleep

from arbi_agent.agent import arbi_agent_excutor
from new_test.agent_test import TestAgent


if __name__ == '__main__':
    broker_url = "tcp://127.0.0.1:61616"

    sender_agent = TestAgent()
    sender_agent_name = "agent://www.arbi.com/SenderAgent"
    receiver_agent_name = "agent://www.arbi.com/ReceiverAgent"
    arbi_agent_excutor.excute(broker_url, agent_name=sender_agent_name, agent=sender_agent, broker_type=2)
    print("sender agent ready")

    print("test start!")

    input()
    # agent1 send test message to agent2
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