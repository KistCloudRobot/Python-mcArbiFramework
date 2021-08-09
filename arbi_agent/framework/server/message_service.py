from arbi_agent.configuration import BrokerType, LTMMessageAction
from arbi_agent.agent.arbi_agent_message import ArbiAgentMessage
from arbi_agent.framework.server.mc_arbi_server_adaptor import McArbiServerAdaptor
from arbi_agent.framework.server.zeromq_server_message_adaptor import ZeroMQServerMessageAdaptor
from arbi_agent.framework.center.ltm_message_processor import LTMMessageProcessor
from arbi_agent.ltm.communication.ltm_message_queue import LTMMessageQueue
from arbi_agent.ltm.communication.zeromq.zeromq_ltm_adaptor import ZeroMQLTMAdaptor
from arbi_agent.ltm.ltm_message import LTMMessage


class MessageService:
    def __init__(self, server_name: str, broker_type: int):
        if broker_type == 2:
            self.deliver_adaptor = ZeroMQServerMessageAdaptor(self, server_name)
        elif broker_type == 0:
            self.deliver_adaptor = McArbiServerAdaptor(self)
        
        self.ltm_listener = self.deliver_adaptor
        self.broker_type = broker_type

        self.ltm_message_processor = LTMMessageProcessor(self)

        self.ltm_adaptor = None

    def initialize(self, broker_url: str, center_url: str):
        self.deliver_adaptor.initialize(broker_url, center_url)
        queue = LTMMessageQueue()
        if self.broker_type == BrokerType.ZERO_MQ or self.broker_type == BrokerType.MC or self.broker_type == 2 or self.broker_type == 0:
            self.ltm_adaptor = ZeroMQLTMAdaptor(broker_url, "tcp://ltmServer", queue)

    def message_received(self, message):
        if type(message) is ArbiAgentMessage:
            self.deliver_adaptor.deliver(message)
        elif type(message) is LTMMessage:
            if message.get_action() == LTMMessageAction.Notify:
                self.ltm_listener.send(message)
            else:
                self.ltm_message_processor.on_message(message)

    def send(self, message):
        self.ltm_listener.send(message)

    def notify(self, message):
        self.ltm_adaptor.send(message)
