from time import sleep

from arbi_agent.agent.arbi_agent import ArbiAgent
from arbi_agent.agent import arbi_agent_executor
from arbi_agent.ltm.data_source import DataSource


class TimeGetTest(ArbiAgent):
    def __init__(self):
        arbi_agent_executor.execute("tcp://127.0.0.1:61616", "agent://www.arbi.com/TestAgent", self, 2)

    def on_start(self):
        print("start")

        ds = DataSource()
        ds.connect("tcp://127.0.0.1:61616", "timeGetTest", 2)
        ds.assert_fact("(testFact \"testing\")")

        sleep(1)

        timestamp = ds.get_last_modified_time("(testFact \"testing\")")
        print(timestamp)
        print(type(timestamp))

        timestamp = ds.get_last_modified_time("(testtest \"asdf\")")
        print(timestamp)
        print(type(timestamp))


if __name__ == '__main__':
    TimeGetTest()
