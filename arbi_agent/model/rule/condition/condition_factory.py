from arbi_agent.configuration import ConditionType
from arbi_agent.model.rule.condition.condition import Condition
from arbi_agent.model.rule.condition.condition_event import EventCondition
from arbi_agent.model.rule.condition.condition_expression import ExpressionCondition
from arbi_agent.model.rule.condition.condition_fact import FactCondition
from arbi_agent.model.rule.condition.condition_post import PostCondition
from arbi_agent.model.rule.condition.condition_retracted import RetractedCondition

def new_condition_from_gl(gl_condition) :

    if gl_condition.get_name() == ConditionType.TYPE_FACT :
        if gl_condition.get_expression_size() == 1 :
            predicate_expression = gl_condition.get_expression(0)
            if predicate_expression.is_generalized_list() :
                return FactCondition(predicate_expression.as_generalized_list())
        return None

    elif gl_condition.get_name() == ConditionType.TYPE_EXPRESSION :
        if gl_condition.get_expression_size() == 1 :
            return ExpressionCondition(gl_condition.get_expression(0))
        return None

    elif gl_condition.get_name() == ConditionType.TYPE_POST :
        if gl_condition.get_expression_size() == 1 :
            event_expression = gl_condition.get_expression(0)
            if event_expression.is_generalized_list() :
                return PostCondition(event_expression.as_generalized_list())
        return None

    elif gl_condition.get_name() == ConditionType.TYPE_EVENT :
        if gl_condition.get_expression_size() == 1 :
            event_expression = gl_condition.get_expression(0)
            if event_expression.is_generalized_list() :
                return EventCondition(event_expression.as_generalized_list())
        return None

    elif gl_condition.get_name() == ConditionType.TYPE_RETRACT :
        if gl_condition.get_expression_size() == 1 :
            retracted_expression = gl_condition.get_expression(0)
            if retracted_expression.is_generalized_list() :
                return RetractedCondition(retracted_expression.as_generalized_list())
        return None

    return None

def new_condition_from_gl_string(event) :
    import arbi_agent.model.generalized_list_factory as GLFactory
    gl = GLFactory.new_gl_from_gl_string(event)
    return new_condition_from_gl(gl)

def to_fact_string(condition) :
    condition_string = "(fact (" + condition.get_predicate_name()
    for expression in condition.get_expressions() :
        condition_string = condition_string + " " + str(expression)
    condition_string = condition_string + "))"
    return condition_string