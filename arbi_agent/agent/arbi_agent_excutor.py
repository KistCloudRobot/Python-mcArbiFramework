from arbi_agent.agent.arbi_agent import ArbiAgent
from arbi_agent.configuration import BrokerType


def execute(agent_name: str, agent: ArbiAgent, broker_type: int):
    agent.initialize(agent_url=agent_name, broker_type=broker_type)


def execute(broker_url: str, agent_name: str, agent: ArbiAgent, broker_type: int):
    agent.initialize(broker_url=broker_url, agent_url=agent_name, broker_type=broker_type)
