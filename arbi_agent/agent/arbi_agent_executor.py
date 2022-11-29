from arbi_agent.agent.arbi_agent import ArbiAgent
from arbi_agent.configuration import BrokerType

# def execute(agent_name: str, agent: ArbiAgent, broker_type: BrokerType, daemon=True):
#     agent.initialize(agent_url=agent_name, broker_type=broker_type, daemon=daemon)

def execute(broker_host: str, broker_port: int, agent_name: str, agent: ArbiAgent, broker_type: BrokerType, daemon=True):
    agent.initialize(broker_host=broker_host, broker_port=broker_port, agent_uri=agent_name, broker_type=broker_type, daemon=daemon)
