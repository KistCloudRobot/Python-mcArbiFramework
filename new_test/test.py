from arbi_agent.agent.arbi_agent import ArbiAgent
from arbi_agent.ltm.data_source import DataSource
from arbi_agent.agent import arbi_agent_excutor
from arbi_agent.model import generalized_list_factory


class MyDataSource(DataSource):
    def on_notify(self, content):
        print("on notify :", content)
        gl = generalized_list_factory.new_gl_from_gl_string(content)
        val = gl.get_expression(1).as_value().float_value()
        print(val)
        val = gl.get_expression(3)
        print(val)
        val = val.as_value().boolean_value()
        print(val)


class TestAgent(ArbiAgent):
    def __init__(self):
        super().__init__()

    def close(self):
        super().close()

    def on_start(self):
        dc = MyDataSource()
        dc.connect("tcp://127.0.0.1:61616", "ds://test_ds", 2)

        subscribe_rule = "(rule (fact (RobotInfo $robot_id $x $y $loading $speed $batterty)) --> " \
                         "(notify (RobotInfo $robot_id $x $y $loading $speed $batterty)))"

        dc.subscribe(subscribe_rule)

        dc.assert_fact("(RobotInfo \"ID01\" 1.1 40 \"False\" 3.4 \"stable\")")

        input()

        dc.close()


if __name__ == "__main__":
    agent = TestAgent()
    arbi_agent_excutor.excute(broker_url="tcp://127.0.0.1:61616", agent_name="agent://www.arbi.com/LTMTestAgent",
                              agent=agent, broker_type=2)
    agent.close()
