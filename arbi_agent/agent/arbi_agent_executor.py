from arbi_agent.agent.arbi_agent import ArbiAgent
from arbi_agent.configuration import BrokerType


def execute(agent_name: str, agent: ArbiAgent, broker_type: BrokerType, daemon=True):
    agent.initialize(agent_url=agent_name, broker_type=broker_type, daemon=daemon)


def execute(broker_url: str, agent_name: str, agent: ArbiAgent, broker_type: BrokerType, daemon=True):
    agent.initialize(broker_url=broker_url, agent_url=agent_name, broker_type=broker_type, daemon=daemon)
