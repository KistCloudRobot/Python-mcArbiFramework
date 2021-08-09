import time
import base64

from arbi_agent.agent.logger.action_body import ActionBody
from arbi_agent.configuration import LoggerContents


class LoggingActionNonAction(ActionBody):
    def __init__(self, agent, actor: str, action: str):
        self.agent = agent
        self.actor = actor
        self.action = action

    def excute(self, obj) -> object:
        self.send_log(str(obj))
        return obj

    def send_log(self, content: str):
        current_time = round(time.time() * 1000)
        encoded_content = base64.b64encode(content.encode('utf-8'))

        print(LoggerContents.INTERACTION_MANAGER_ADDRESS,
              "[System Log]	(SystemLog (actor \"" + self.actor + "\") "
              + "(action \"" + self.action + "\") "
              + "(content \"" + str(encoded_content) + "\") "
              + "(time \"" + str(current_time) + "\"))")

        self.agent.system(LoggerContents.INTERACTION_MANAGER_ADDRESS,
                          "(SystemLog (actor \"" + self.actor + "\") "
                          + "(action \"" + self.action + "\") "
                          + "(content \"" + str(encoded_content) + "\") "
                          + "(time \"" + str(current_time) + "\"))")
