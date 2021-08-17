from arbi_agent.agent.arbi_agent import ArbiAgent
from arbi_agent.agent import arbi_agent_excutor
from arbi_agent.agent.logger.agent_action import AgentAction
from arbi_agent.agent.logger.action_body import ActionBody
from arbi_agent.agent.logger.logger_manager import LoggerManager
from arbi_agent.agent.logger.log_timing import LogTiming


class TestAction(ActionBody):
    def excute(self, obj) -> object:
        print(obj.get_name())
        return None


class TestArgument:
    def __init__(self, name: str):
        self.name = name

    def get_name(self) -> str:
        return self.name


class TestAgent(ArbiAgent):
    def __init__(self):
        super().__init__()
        arbi_agent_excutor.excute(broker_url="tcp://127.0.0.1:61616", agent_name="agent://www.arbi.com/TestAgent",
                                  agent=self, broker_type=2)

    def on_start(self):
        test_action = AgentAction('test action', TestAction())
        LoggerManager.get_instance().register_action(test_action, LogTiming.Prior)
        test_action.change_action(True)
        LoggerManager.get_instance().get_action('test action').excute(TestArgument('Hi'))


if __name__ == '__main__':
    agent = TestAgent()
    input()
