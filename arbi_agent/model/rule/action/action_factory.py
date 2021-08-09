from arbi_agent.configuration import ActionType
from arbi_agent.model.rule.action.action_notify import Notify
from arbi_agent.model.rule.action.action_stream import Stream

def new_action_from_gl(subscriber, gl_action) :

    if gl_action.get_name() == ActionType.TYPE_NOTIFY :
        if gl_action.get_expression_size() == 1 :
            notification_expression = gl_action.get_expression(0)
            if notification_expression.is_generalized_list() :
                return Notify(subscriber, notification_expression.as_generalized_list())
        return None
    elif gl_action.get_name() == ActionType.TYPE_STEAM :
        if gl_action.get_expression_size() == 1 :
            stream_expression = gl_action.get_expression(0)
            if stream_expression.is_generalized_list() :
                return Stream(subscriber, stream_expression.as_generalized_list())
        return None

    return None