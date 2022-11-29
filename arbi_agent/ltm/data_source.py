from arbi_agent.configuration import BrokerType
from arbi_agent.ltm.communication.data_source_interface_toolkit import DataSourceInterfaceToolkit


class DataSource:
    def __init__(self):
        self.data_source_uri = None
        self.running = False
        self.data_source_interface_toolkit = None

    def connect(self, broker_host: str, broker_port: int, data_source_uri: str, broker_type: BrokerType):
        self.data_source_uri = data_source_uri
        self.running = True
        self.data_source_interface_toolkit = DataSourceInterfaceToolkit(broker_host, broker_port, data_source_uri, self, broker_type)
        self.data_source_interface_toolkit.start()

    def close(self):
        self.data_source_interface_toolkit.close()
        self.running = False

    def assert_fact(self, fact: str):
        self.data_source_interface_toolkit.assert_fact(self.data_source_uri, fact)

    def retract_fact(self, fact: str) -> str:
        return self.data_source_interface_toolkit.retract_fact(self.data_source_uri, fact)

    def retrieve_fact(self, fact: str) -> str:
        return self.data_source_interface_toolkit.retrieve_fact(self.data_source_uri, fact)

    def update_fact(self, fact: str):
        self.data_source_interface_toolkit.update_fact(self.data_source_uri, fact)

    def match(self, fact: str) -> str:
        return self.data_source_interface_toolkit.match(self.data_source_uri, fact)

    def subscribe(self, rule: str) -> str:
        return self.data_source_interface_toolkit.subscribe(self.data_source_uri, rule)

    def unsubscribe(self, subscribe_id: str):
        self.data_source_interface_toolkit.unsubscribe(self.data_source_uri, subscribe_id)

    def on_notify(self, content: str):
        pass

    def get_last_modified_time(self, content: str) -> str:
        return self.data_source_interface_toolkit.get_last_modified_time(self.data_source_uri, content)

    def is_running(self) -> bool:
        return self.running
