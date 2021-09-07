from arbi_agent.configuration import BrokerType
from arbi_agent.ltm.communication.data_source_interface_toolkit import DataSourceInterfaceToolkit


class DataSource:
    def __init__(self):
        self.data_source_url = None
        self.running = False
        self.data_source_interface_toolkit = None

    def connect(self, broker_url: str, data_source_url: str, broker_type: int):
        self.data_source_url = data_source_url
        self.running = True
        self.data_source_interface_toolkit = DataSourceInterfaceToolkit(broker_url, data_source_url, self, broker_type)

    def close(self):
        self.data_source_interface_toolkit.close()
        self.running = False

    def assert_fact(self, fact: str):
        self.data_source_interface_toolkit.assert_fact(self.data_source_url, fact)

    def retract_fact(self, fact: str) -> str:
        return self.data_source_interface_toolkit.retract_fact(self.data_source_url, fact)

    def retrieve_fact(self, fact: str) -> str:
        return self.data_source_interface_toolkit.retrieve_fact(self.data_source_url, fact)

    def update_fact(self, fact: str):
        self.data_source_interface_toolkit.update_fact(self.data_source_url, fact)

    def match(self, fact: str) -> str:
        return self.data_source_interface_toolkit.match(self.data_source_url, fact)

    def subscribe(self, rule: str) -> str:
        return self.data_source_interface_toolkit.subscribe(self.data_source_url, rule)

    def unsubscribe(self, subscribe_id: str):
        self.data_source_interface_toolkit.unsubscribe(self.data_source_url, subscribe_id)

    def on_notify(self, content: str):
        pass

    def get_last_modified_time(self, content: str) -> str:
        return self.data_source_interface_toolkit.get_last_modified_time(self.data_source_url, content)

    def is_running(self) -> bool:
        return self.running
