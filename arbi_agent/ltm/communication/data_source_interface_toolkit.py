from multiprocessing.pool import ThreadPool
import threading

from arbi_agent.configuration import LTMMessageAction, LTMConstants
from arbi_agent.ltm.ltm_message import LTMMessage
from arbi_agent.ltm.communication.adaptor.zeromq_ltm_adaptor import ZeroMQLTMAdaptor
from arbi_agent.ltm.communication.adaptor.activemq_ltm_adaptor import ActiveMQLTMAdaptor
from arbi_agent.ltm.communication.ltm_message_queue import LTMMessageQueue
from arbi_agent.configuration import BrokerType


class DataSourceInterfaceToolkit:

    def __init__(self, broker_host, broker_port, data_source_uri, data_source, broker_type: BrokerType):
        self.data_source = data_source
        self.queue = LTMMessageQueue()

        if broker_type == BrokerType.ZERO_MQ:
            self.adaptor = ZeroMQLTMAdaptor(broker_host, broker_port, data_source_uri, self.queue)
        elif broker_type == BrokerType.ACTIVE_MQ:
            self.adaptor = ActiveMQLTMAdaptor(broker_host, broker_port, data_source_uri, self.queue)
        else:
            raise Exception("undefined broker type : " + str(broker_type))

        self.waiting_result = list()

        self.executor = ThreadPool(processes=LTMConstants.TOOLKIT_THREAD_NUMBER)

        self.toolkit_thread = threading.Thread(target=self.run, args=())
        self.toolkit_thread.daemon = True

    def start(self):
        self.toolkit_thread.start()
        self.adaptor.start()

    def run(self):
        while self.data_source.is_running():
            message = self.queue.blocking_dequeue(None, 0.5)
            if message is not None:
                self.dispatch(message)

    def close(self):
        self.adaptor.close()

    def dispatch(self, message: LTMMessage):
        action = message.get_action()
        if action == LTMMessageAction.Notify:
            self.executor.apply_async(self.dispatch_on_notify, (message, ))
        else:
            self.dispatch_response(message)

    def dispatch_response(self, message: LTMMessage):
        response_message = None
        for waiting_message in self.waiting_result:
            if message.get_conversation_id() == waiting_message.get_conversation_id():
                response_message = waiting_message
                break
        response_message.set_response(message)
        self.waiting_result.remove(response_message)

    def dispatch_on_notify(self, message: LTMMessage):
        self.on_notify(message.get_content())

    def on_notify(self, content):
        self.data_source.on_notify(content)

    def assert_fact(self, url: str, fact: str):
        message = LTMMessage(client=url, action=LTMMessageAction.AssertFact, content=fact)
        self.waiting_result.append(message)
        self.adaptor.send(message)

    def retract_fact(self, url: str, fact: str) -> str:
        message = LTMMessage(client=url, action=LTMMessageAction.RetractFact, content=fact)
        self.waiting_result.append(message)
        self.adaptor.send(message)
        return message.get_response()

    def retrieve_fact(self, url: str, fact: str) -> str:
        message = LTMMessage(client=url, action=LTMMessageAction.RetrieveFact, content=fact)
        self.waiting_result.append(message)
        self.adaptor.send(message)
        return message.get_response()

    def update_fact(self, url: str, fact: str):
        message = LTMMessage(client=url, action=LTMMessageAction.UpdateFact, content=fact)
        self.waiting_result.append(message)
        self.adaptor.send(message)

    def match(self, url: str, fact: str) -> str:
        message = LTMMessage(client=url, action=LTMMessageAction.Match, content=fact)
        self.waiting_result.append(message)
        self.adaptor.send(message)
        return message.get_response()

    def subscribe(self, url: str, rule: str) -> str:
        message = LTMMessage(client=url, action=LTMMessageAction.Subscribe, content=rule)
        self.waiting_result.append(message)
        self.adaptor.send(message)
        return message.get_response()

    def unsubscribe(self, url: str, subscribe_id: str):
        message = LTMMessage(client=url, action=LTMMessageAction.Unsubscribe, content=subscribe_id)
        self.waiting_result.append(message)
        self.adaptor.send(message)

    def get_last_modified_time(self, url: str, content: str) -> str:
        message = LTMMessage(client=url, action=LTMMessageAction.GetLastModifiedTime, content=content)
        self.waiting_result.append(message)
        self.adaptor.send(message)
        return message.get_response()
