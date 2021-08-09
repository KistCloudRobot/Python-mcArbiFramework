import threading

from ...configuration import BrokerType, LTMMessageAction
from .zeromq.zeromq_ltm_adaptor import ZeroMQLTMAdaptor
from .ltm_message_queue import LTMMessageQueue
from ..ltm_message import LTMMessage


class DataSourceInterfaceToolkit:

    def __init__(self, broker_url, data_source_url, data_source, broker_type: int):
        self.data_source = data_source
        self.queue = LTMMessageQueue()

        if broker_type == 2:
            self.adaptor = ZeroMQLTMAdaptor(broker_url, data_source_url, self.queue)

        self.waiting_result = list()

        self.toolkit_thread = threading.Thread(target=self.run, args=())
        self.toolkit_thread.daemon = True
        self.toolkit_thread.start()

    def run(self):
        while self.data_source.is_running():
            message = self.queue.blocking_dequeue(None, 0.5)
            if message is not None:
                self.dispatch(message)

    def close(self):
        self.adaptor.close()

    def dispatch(self, message):
        if message.get_action() == LTMMessageAction.Notify:
            self.data_source.on_notify(message.get_content())
            return
        else:
            for waiting_message in self.waiting_result:
                if message.get_conversation_id() == waiting_message.get_conversation_id():
                    waiting_message.set_response(message)
                    self.waiting_result.remove(waiting_message)
                    break

    def assert_fact(self, url, fact):
        message = LTMMessage(client=url, action=LTMMessageAction.AssertFact, content=fact)
        self.waiting_result.append(message)
        self.adaptor.send(message)

    def retract_fact(self, url, fact):
        message = LTMMessage(client=url, action=LTMMessageAction.RetractFact, content=fact)
        self.waiting_result.append(message)
        self.adaptor.send(message)
        return message.get_response()

    def retrieve_fact(self, url, fact):
        message = LTMMessage(client=url, action=LTMMessageAction.RetrieveFact, content=fact)
        self.waiting_result.append(message)
        self.adaptor.send(message)
        return message.get_response()

    def update_fact(self, url, fact):
        message = LTMMessage(client=url, action=LTMMessageAction.UpdateFact, content=fact)
        self.waiting_result.append(message)
        self.adaptor.send(message)

    def match(self, url, fact):
        message = LTMMessage(client=url, action=LTMMessageAction.Match, content=fact)
        self.waiting_result.append(message)
        self.adaptor.send(message)
        return message.get_response()

    def subscribe(self, url, rule):
        message = LTMMessage(client=url, action=LTMMessageAction.Subscribe, content=rule)
        self.waiting_result.append(message)
        self.adaptor.send(message)
        message = message.get_response()
        return message

    def unsubscribe(self, url, subscribe_id):
        message = LTMMessage(client=url, action=LTMMessageAction.Unsubscribe, content=subscribe_id)
        self.waiting_result.append(message)
        self.adaptor.send(message)
