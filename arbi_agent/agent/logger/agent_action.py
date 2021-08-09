from arbi_agent.agent.logger.action_body import ActionBody
from arbi_agent.agent.logger.log_timing import LogTiming
from arbi_agent.agent.logger.logging_action.logging_action_prior import LoggingActionPrior
from arbi_agent.agent.logger.logging_action.logging_action_later import LoggingActionLater
from arbi_agent.agent.logger.logging_action.logging_action_both import LoggingActionBoth
from arbi_agent.agent.logger.logging_action.logging_action_non_action import LoggingActionNonAction


class AgentAction(ActionBody):
    def __init__(self, action_name: str, normal_action: ActionBody):
        self.action_name: str = action_name
        self.normal_action: ActionBody = normal_action
        self.current_action: ActionBody = normal_action
        self.logging_action: ActionBody = None

    def init_logging_function(self, agent, actor: str, log_timing: LogTiming):
        if log_timing is LogTiming.Prior:
            self.logging_action = LoggingActionPrior(agent, actor, self.action_name, self.normal_action)
        elif log_timing is LogTiming.Later:
            self.logging_action = LoggingActionLater(agent, actor, self.action_name, self.normal_action)
        elif log_timing is LogTiming.Both:
            self.logging_action = LoggingActionBoth(agent, actor, self.action_name, self.normal_action)
        elif log_timing is LogTiming.NonAction:
            self.logging_action = LoggingActionNonAction(agent, actor, self.action_name)
        else:
            self.logging_action = LoggingActionPrior(agent, actor, self.action_name, self.normal_action)

    def get_action_name(self) -> str:
        return self.action_name

    def change_action(self, flag: bool):
        if flag:
            self.current_action = self.logging_action
        else:
            self.current_action = self.normal_action

    def get_function(self) -> ActionBody:
        return self.current_action

    def excute(self, obj) -> object:
        return self.current_action.excute(obj)
