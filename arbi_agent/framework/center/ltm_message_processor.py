from arbi_agent.framework.center.ltm_service import LTMService
from arbi_agent.configuration import LTMMessageAction
from arbi_agent.ltm.ltm_message import LTMMessage


class LTMMessageProcessor:
    def __init__(self, message_service):
        self.message_service = message_service
        LTMService.set_notification_handler(self)

        self.command = {
            LTMMessageAction.AssertFact: LTMService.assert_fact,
            LTMMessageAction.RetractFact: LTMService.retract_fact,
            LTMMessageAction.RetrieveFact: LTMService.retrieve_fact,
            LTMMessageAction.UpdateFact: LTMService.update_fact,
            LTMMessageAction.Match: LTMService.match,
            LTMMessageAction.Subscribe: LTMService.subscribe,
            LTMMessageAction.Unsubscribe: LTMService.unsubscribe,
        }

    def notify(self, action):
        notify_message = LTMMessage(client=action.get_subscriber(), action=LTMMessageAction.Notify,
                                    content=action.to_action_content())
        self.message_service.notify(notify_message)

    def on_message(self, msg):
        result = self.command[msg.get_action()](msg.get_client(), msg.get_content())
        result_message = LTMMessage(client=msg.get_client(), action=LTMMessageAction.Result, content=result,
                                    conversation_id=msg.get_conversation_id())
        self.message_service.send(result_message)
