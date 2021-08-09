import threading
import concurrent.futures

from arbi_agent.agent.arbi_agent_message import ArbiAgentMessage
from arbi_agent.agent.communication.arbi_message_queue import ArbiMessageQueue
from arbi_agent.agent.communication.zeromq.zeromq_agent_adaptor import ZeroMQAgentAdaptor
from arbi_agent.configuration import AgentMessageAction, AgentConstants


class ArbiAgentMessageToolkit:
    def __init__(self, broker_url: str, agent_url: str, agent, broker_type: int):
        self.agent_url = agent_url
        self.queue = ArbiMessageQueue()

        self.adaptor = None

        if broker_type == 2:
            self.adaptor = ZeroMQAgentAdaptor(broker_url, agent_url, self.queue)

        self.executer = concurrent.futures.ThreadPoolExecutor(max_workers=AgentConstants.TOOLKIT_THREAD_NUMBER)

        self.wating_response = []

        self.agent = agent

        self.toolkit_thread = threading.Thread(target=self.run, args=())
        self.toolkit_thread.daemon = True
        self.toolkit_thread.start()

    def close(self):
        self.adaptor.close()

    def create_message(self, receiver, action, content) -> ArbiAgentMessage:
        return ArbiAgentMessage(sender=self.agent_url, receiver=receiver, action=action, content=content)

    def run(self):
        while self.agent.is_running():
            message = self.queue.blocking_dequeue(None, 0.5)
            if message is not None:
                self.dispatch(message)

    def dispatch(self, message: ArbiAgentMessage):
        action = message.get_action()

        if action == AgentMessageAction.Inform:
            self.executer.submit(self.dispatch_data_task, message)
        elif action == AgentMessageAction.Request:
            self.executer.submit(self.dispatch_request_task, message)
        elif action == AgentMessageAction.Query:
            self.executer.submit(self.dispatch_query_task, message)
        elif action == AgentMessageAction.Notify:
            self.executer.submit(self.dispatch_notify_task, message)
        elif action == AgentMessageAction.Subscribe:
            self.executer.submit(self.dispatch_subscribe_task, message)
        elif action == AgentMessageAction.Unsubscribe:
            self.executer.submit(self.dispatch_unsubscribe_task, message)
        elif action == AgentMessageAction.System:
            self.executer.submit(self.dispatch_system_task, message)
        # elif action == AgentMessageAction.ACTION_REQUEST_STREAM:
        #     self.executer.submit(self.dispatch_request_stream_task, message)
        # elif action == AgentMessageAction.ACTION_RELEASE_STREAM:
        #     self.executer.submit(self.dispatch_release_stream_task, message)
        elif action == AgentMessageAction.Response:
            self.executer.submit(self.dispatch_response, message)
        else:
            print("message toolkit: dispatch: MESSAGE TYPE ERROR")

    def dispatch_response(self, message: ArbiAgentMessage):
        response_message = None
        for waiting_message in self.wating_response:
            if message.get_conversation_id() == waiting_message.get_conversation_id():
                response_message = waiting_message
                break
        response_message.set_response(message)
        self.wating_response.remove(response_message)

    def dispatch_data_task(self, message):
        sender = message.get_sender()
        data = message.get_content()
        self.on_data(sender, data)

    def dispatch_notify_task(self, message):
        sender = message.get_sender()
        data = message.get_content()
        self.on_notify(sender, data)

    def dispatch_query_task(self, message):
        request_id = message.get_conversation_id()
        sender = message.get_sender()
        query = message.get_content()

        response = self.on_query(sender, query)

        if response is None:
            response = "ok"

        self.send_response_message(request_id, sender, response)

    # def dispatch_release_stream_task(self, message):
    #     sender = message.get_sender()
    #     stream_id = message.get_content()
    #     self.on_release_stream(sender, stream_id)

    # def dispatch_request_stream_task(self, message):
    #     request_id = message.get_conversation_id()
    #     sender = message.get_sender()
    #     rule = message.get_content()

    #     response = self.on_request_stream(sender, rule)

    #     if response == None:
    #         response = "ok"

    #    self.send_response_message(request_id, sender, response)

    def dispatch_request_task(self, message):
        request_id = message.get_conversation_id()
        sender = message.get_sender()
        request = message.get_content()

        response = self.on_request(sender, request)

        if response is None:
            response = "ok"

        self.send_response_message(request_id, sender, response)

    def dispatch_subscribe_task(self, message):
        request_id = message.get_conversation_id()
        sender = message.get_sender()
        request = message.get_content()

        response = self.on_subscribe(sender, request)

        if response is None:
            response = "ok"

        self.send_response_message(request_id, sender, response)

    def dispatch_system_task(self, message):
        sender = message.get_sender()
        data = message.get_content()
        self.on_system(sender, data)

    def dispatch_unsubscribe_task(self, message):
        sender = message.get_sender()
        request = message.get_content()
        self.on_unsubscribe(sender, request)

    def send_response_message(self, request_id, sender, response):
        message = ArbiAgentMessage(sender=self.agent_url, receiver=sender, action=AgentMessageAction.Response,
                                   content=response, conversation_id=request_id)
        self.adaptor.send(message)

    def request(self, receiver, content):
        message = self.create_message(receiver, AgentMessageAction.Request, content)
        self.wating_response.append(message)
        self.adaptor.send(message)
        return message.get_response()

    def query(self, receiver, content):
        message = self.create_message(receiver, AgentMessageAction.Query, content)
        self.wating_response.append(message)
        self.adaptor.send(message)
        return message.get_response()

    def send(self, receiver, content):
        message = self.create_message(receiver, AgentMessageAction.Inform, content)
        self.adaptor.send(message)

    def subscribe(self, receiver, content):
        message = self.create_message(receiver, AgentMessageAction.Subscribe, content)
        self.wating_response.append(message)
        self.adaptor.send(message)
        return message.get_response()

    def unsubscribe(self, receiver, content):
        message = self.create_message(receiver, AgentMessageAction.Unsubscribe, content)
        self.adaptor.send(message)

    def notify(self, receiver, content):
        message = self.create_message(receiver, AgentMessageAction.Notify, content)
        self.adaptor.send(message)

    def system(self, receiver, content):
        message = self.create_message(receiver, AgentMessageAction.System, content)
        self.adaptor.send(message)

    # def request_stream(self, receiver, content):
    #     message = self.create_message(receiver, AgentMessageAction.ACTION_REQUEST_STREAM, content)
    #     self.wating_response.append(message)
    #     self.adaptor.send(message)
    #     return message.get_response()

    # def release_stream(self, receiver, content):
    #     message = self.create_message(receiver, AgentMessageAction.ACTION_RELEASE_STREAM, content)
    #     self.adaptor.send(message)

    def on_request(self, sender, request):
        return self.agent.on_request(sender, request)

    def on_query(self, sender, query):
        return self.agent.on_query(sender, query)

    def on_data(self, sender, data):
        self.agent.on_data(sender, data)

    def on_notify(self, sender, data):
        self.agent.on_notify(sender, data)

    def on_unsubscribe(self, sender, unsubscribe):
        self.agent.on_unsubscribe(sender, unsubscribe)

    def on_subscribe(self, sender, subscribe):
        return self.agent.on_subscribe(sender, subscribe)

    def on_system(self, sender, data):
        self.agent.on_system(sender, data)

    # def on_request_stream(self, sender, rule):
    #     return self.agent.on_request_stream(sender, rule)

    # def on_release_stream(self, sender, stream_id):
    #     self.agent.on_release_stream(sender, stream_id)
