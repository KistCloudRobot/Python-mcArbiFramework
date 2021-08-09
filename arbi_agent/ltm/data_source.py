from ..configuration import BrokerType
from .communication.data_source_interface_toolkit import DataSourceInterfaceToolkit


class DataSource:
    def __init__(self):
        self.data_source_url = None
        self.running = False
        self.data_source_interface_toolkit = None

    def connect(self, broker_url, data_source_url, broker_type: int):
        self.data_source_url = data_source_url
        self.running = True
        self.data_source_interface_toolkit = DataSourceInterfaceToolkit(broker_url, data_source_url, self, broker_type)

    def close(self):
        self.data_source_interface_toolkit.close()
        self.running = False

    def assert_fact(self, fact):
        self.data_source_interface_toolkit.assert_fact(self.data_source_url, fact)

    def retract_fact(self, fact):
        return self.data_source_interface_toolkit.retract_fact(self.data_source_url, fact)

    def retrieve_fact(self, fact):
        return self.data_source_interface_toolkit.retrieve_fact(self.data_source_url, fact)

    def update_fact(self, fact):
        self.data_source_interface_toolkit.update_fact(self.data_source_url, fact)

    def match(self, fact):
        return self.data_source_interface_toolkit.match(self.data_source_url, fact)

    def subscribe(self, rule):
        return self.data_source_interface_toolkit.subscribe(self.data_source_url, rule)

    def unsubscribe(self, subscribe_id):
        self.data_source_interface_toolkit.unsubscribe(self.data_source_url, subscribe_id)

    def on_notify(self, content):
        pass

    def is_running(self):
        return self.running
