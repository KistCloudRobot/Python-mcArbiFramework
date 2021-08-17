from arbi_agent.agent.arbi_agent import ArbiAgent
from arbi_agent.ltm.data_source import DataSource
from arbi_agent.agent import arbi_agent_excutor
from arbi_agent.model import generalized_list_factory as GLFactory


class MyDataSource(DataSource):
    def on_notify(self, content):
        print("on notify : " + content)
        gl = GLFactory.new_gl_from_gl_string(content)
        val = gl.get_expression(0).as_value().int_value()
        print("val :", val, ", type :", type(val))


class TestAgent(ArbiAgent):
    def __init__(self):
        super().__init__()

    def close(self):
        super().close()

    def on_start(self):
        dc = MyDataSource()
        dc.connect("tcp://127.0.0.1:61616", "ds://test_ds", 2)

        input()
        print("assert fact (test \"test1\")")
        dc.assert_fact("(test \"test1\")")

        input()
        print("retrieve fact (test $var)")
        result = dc.retrieve_fact("(test $var)")
        print("result : " + result)

        input()
        print("retract fact (test $var)")
        result = dc.retract_fact("(test $var)")
        print("result : " + result)

        input()
        print("retrieve fact (test $var)")
        result = dc.retrieve_fact("(test $var)")
        print("result : " + result)

        input()
        print("subscribe (fact (test $var))")
        subscribe_id = dc.subscribe("(rule (fact (test $var)) --> (notify (test $var)))")

        input()
        print("assert fact (test 3)")
        dc.assert_fact("(test 3)")

        input()
        print("update fact (test \"test2\") to (test \"test3\"))")
        dc.update_fact("(update (test $var) (test \"test3\"))")

        input()
        print("assert fact (testtest \"test1\")")
        dc.assert_fact("(testest \"test1\")")

        input()
        print("unsubscribe")
        dc.unsubscribe(subscribe_id)

        input()
        print("update fact update (test \"test3\") to (test \"test4\")")
        dc.update_fact("(update (test $var) (test \"test4\"))")

        input()
        print("test finished")
        dc.close()


if __name__ == "__main__":
    agent = TestAgent()
    arbi_agent_excutor.excute(broker_url="tcp://127.0.0.1:61616", agent_name="agent://www.arbi.com/LTMTestAgent",
                              agent=agent, broker_type=2)
    agent.close()
