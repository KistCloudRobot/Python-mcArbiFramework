import json

from arbi_agent.agent.logger.agent_action import AgentAction
from arbi_agent.agent.logger.log_timing import LogTiming


class LoggerManager:
    __logger_manager = None

    @classmethod
    def get_instance(cls):
        if not isinstance(cls.__logger_manager, cls):
            cls.__logger_manager = LoggerManager()
        return cls.__logger_manager

    def __init__(self):
        self.agent = None
        self.actor = None
        self.action_map = dict()

    def init_logger_manager(self, broker_url: str, agent_uri: str, broker_type: int, agent):
        self.agent = agent
        self.actor = agent_uri

    def get_action(self, action_name: str) -> AgentAction:
        if action_name in self.action_map.keys():
            return self.action_map.get(action_name)
        else:
            return None

    def register_action(self, action: AgentAction, log_timing: LogTiming):
        if self.get_action(action.get_action_name()) is None:
            action.init_logging_function(self.agent, self.actor, log_timing)
            self.action_map[action.get_action_name()] = action

    def registor_action(self, action: AgentAction):
        self.register_action(action, LogTiming.NonAction)

    def free_action(self, action_name: str):
        if action_name in self.action_map.keys():
            self.action_map.pop(action_name)

    def change_filter_option(self, data: str):
        filters: dict = json.loads(data)
        action_name: str = filters.get('Action')
        flag = filters.get('Flag')
        if flag.lower() == 'true':
            flag = True
        else:
            flag = False
        action: AgentAction = self.get_action(action_name)
        if action is not None:
            action.change_action(flag)


