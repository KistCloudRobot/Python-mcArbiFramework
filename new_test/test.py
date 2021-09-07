from arbi_agent.agent.arbi_agent import ArbiAgent
from arbi_agent.ltm.data_source import DataSource
from arbi_agent.agent import arbi_agent_excutor
from arbi_agent.model import generalized_list_factory


class MyDataSource(DataSource):
    def __init__(self):
        self.connect("tcp://127.0.0.1:61616", "ds://test_ds", 2)
        self.subscribe("(rule (fact (test $x)) --> (notify (test $x)))")
        self.assert_fact("(test 1)")
        gl = self.retrieve_fact("(test $x)")
        print(gl)

    def on_notify(self, content):
        gl = self.retrieve_fact("(test $x)")
        print(gl)


class TestAgent(ArbiAgent):
    def __init__(self):
        super().__init__()

    def close(self):
        super().close()

    def on_start(self):
        dc = MyDataSource()

        subscribe_rule = "(rule (fact (RobotInfo $robot_id)) --> " \
                         "(notify (RobotInfo $robot_id)))"

        input()

        dc.close()


if __name__ == "__main__":
    agent = TestAgent()
    arbi_agent_excutor.execute(broker_url="tcp://127.0.0.1:61616", agent_name="agent://www.arbi.com/LTMTestAgent",
                              agent=agent, broker_type=2)
    agent.close()
