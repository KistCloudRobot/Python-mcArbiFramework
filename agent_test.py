import sys
import os
from arbi_agent.agent.arbi_agent import ArbiAgent
from arbi_agent.configuration import BrokerType
from time import sleep
from threading import Condition
import arbi_agent.model.parser.gl_parser_implementation as GLParser

from arbi_agent.ltm.data_source import DataSource


class TestAgent(ArbiAgent):
    def __init__(self):
        super().__init__()
        self.lock = Condition()

    def on_data(self, sender, data):
        print("on data : " + data)
        with self.lock:
            self.lock.notify_all()

    def on_request(self, sender, request):
        print("on request : " + request)
        with self.lock:
            self.lock.notify_all()
        print("send response : (test response from python)")
        return "(test response from python)"

    def on_query(self, sender, query):
        print("on query : " + query)
        with self.lock:
            self.lock.notify_all()
        print("send response : (test query response from python)")
        return "(test query response from python)"

    def agent_to_agent_test(self):
        message = "(test send from python)"
        print("send :", message)
        self.send("agent://jam_agent", message)
        sleep(1)
        with self.lock:
            self.lock.wait()
        sleep(1)
        message = "(test request from python)"
        print("request :", message)
        response = self.request("agent://jam_agent", message)
        print("response :", response)
        sleep(1)
        with self.lock:
            self.lock.wait()
        sleep(1)
        message = "(test query from python)"
        print("query :", message)
        response = self.query("agent://jam_agent", message)
        print("response : " + response)
        with self.lock:
            self.lock.wait()

# class TestDS(DataSource) :

#     def on_notify(self, content) :
#         print("notification arrived")
#         print(content)
#         gl = GLParser.parse_generalized_list(content)
#         print(gl.get_name())
#         print(str(gl.get_expression(0)))


if __name__ == "__main__":
    agent = TestAgent()
    agent.initialize(agent_url = "agent://python_agent", broker_url = "tcp://127.0.0.1:61616", broker_type = BrokerType.TYPE_ZERO)
    
    print("agent ready")

    input()

    print('start')
    agent.agent_to_agent_test()

    input()

    # agent.request("agent://conversation_agent", "(request \"something\")")

    # ds = TestDS()
    # ds.connect("tcp://127.0.0.1:61616", "ds://test_ds", BrokerType.TYPE_ZERO)

    # sleep(1)


    # ds.subscribe("(rule (fact (context $var)) --> (notify (context $var)))")

    # sleep(1)

    # ds.assert_fact('(context (hasUncle "x" "y"))')

    # sleep(1)

    # agent2 = TestAgent()
    # agent2.initialize(agent_url = "agent://test_agent2", broker_url = "tcp://127.0.0.1:61616", broker_type = BrokerType.TYPE_ZERO)

    # agent2.send("agent://python_agent", "(test (\"test message\"))")

    # print("check redis")

    # sleep(5)
    # print("retract")

    # ds.retract_fact('(TestGL "TestData")')

    # print("finish")

    # sub_id = ds.subscribe("(rule (fact (TestModel $model)) --> (notify (TestModel $model)))")

    # print(sub_id)

    # sleep(1)

    # ds.assert_fact('(TestModel "TestModel")')

    # sleep(1)

    # ds.unsubscribe(sub_id)

    # sleep(1)

    # ds.assert_fact("(TestModel \"TestModel2\")")

    # sleep(1)

    # result = ds.retrieve_fact("(TestModel $a)")

    # print(result)

    # sleep(1)

    # data = ds.match("(TestModel $a)")

    # print(data)

    # sleep(1)

    # ds.retract_fact('(TestModel "TestModel")')

    # sleep(1)

    # result = ds.retrieve_fact("(TestModel $a)")

    # print(result)

    # sleep(1)

    # ds.update_fact("(update (TestModel $a) (newTestModel $a))")

    # sleep(1)

    # result = ds.retrieve_fact("(newTestModel $a)")

    # print(result)