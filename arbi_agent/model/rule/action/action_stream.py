from arbi_agent.model.rule.action.action import Action

class Stream(Action) :

    def __init__(self, subscriber, stream_form) :
        self.subscriber = subscriber
        self.stream_form = stream_form

    def get_subscriber(self) :
        return self.subscriber

    def to_action_content(self) :
        gl = self.stream_form.evaluate(self.bind)
        return str(gl)

    def bind(self, binding) :
        self.binding = binding