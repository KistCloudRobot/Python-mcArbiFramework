from arbi_agent.model.rule.action.action import Action

class Notify(Action) :

    def __init__(self, subscriber, notification_form) :
        self.subscriber = subscriber
        self.notification_form = notification_form

    def get_subscriber(self) :
        return self.subscriber

    def to_action_content(self) :
        gl = self.notification_form.evaluate(self.binding)
        return str(gl)

    def bind(self, binding) :
        self.binding = binding