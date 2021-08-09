from arbi_agent.framework.center.command.ltm_command import LTMCommand


class SubscribeCommand(LTMCommand):

    def deploy(self, ltm_service, author, fact):
        return ltm_service.subscribe(author, fact)
