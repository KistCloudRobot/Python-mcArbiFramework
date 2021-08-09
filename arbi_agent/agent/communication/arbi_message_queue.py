import threading
import queue
import time

from arbi_agent.agent.arbi_agent_message import ArbiAgentMessage


class ArbiMessageQueue:
    def __init__(self):
        self.queue = queue.Queue()
        self.lock = threading.Condition()

    def enqueue(self, message: ArbiAgentMessage):
        with self.lock:
            self.queue.put(message)
            self.lock.notify_all()

    def dequeue(self, identifier: str) -> ArbiAgentMessage:
        with self.lock:
            if identifier is None:
                if self.queue.empty():
                    return None
                return self.queue.get()

            for message in self.queue.queue:
                if identifier == message.get_conversation_id():
                    self.queue.queue.remove(message)
                    return message

            return None

    def blocking_dequeue(self, identifier: str, time_out: float) -> ArbiAgentMessage:
        with self.lock:
            message = self.dequeue(identifier)

            time_to_wait = time_out

            while message is None:
                start_time = time.time()

                if time_to_wait == 0:
                    self.lock.wait()
                else:
                    self.lock.wait(time_to_wait)

                elaped_time = time.time() - start_time

                message = self.dequeue(identifier)

                if time_out != 0:
                    time_to_wait = time_to_wait - elaped_time
                    if time_to_wait <= 0:
                        break

            return message
