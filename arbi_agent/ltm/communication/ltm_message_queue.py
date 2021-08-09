import threading
import queue
import time


class LTMMessageQueue:
    
    def __init__(self):
        self.queue = queue.Queue()
        self.lock = threading.Condition()

    def enqueue(self, message):
        with self.lock:
            self.queue.put(message)
            self.lock.notify_all()
    
    def dequeue(self, id):
        with self.lock:
            if id is None:
                if self.queue.empty():
                    return None
                return self.queue.get()

            for message in self.queue.queue:
                if id == message.get_conversation_id():
                    self.queue.queue.remove(message)
                    return message

            return None

    def blocking_dequeue(self, id, time_out):
        with self.lock:
            message = self.dequeue(id)
            time_to_wait = time_out

            while message is None:
                start_time = time.time()

                if time_to_wait == 0:
                    self.lock.wait()
                else:
                    self.lock.wait(time_to_wait)
                
                elaped_time = time.time() - start_time
                
                message = self.dequeue(id)

                if time_out != 0:
                    time_to_wait = time_to_wait - elaped_time
                    if time_to_wait <= 0:
                        break

            return message
