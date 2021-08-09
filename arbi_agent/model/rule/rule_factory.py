from arbi_agent.model.rule.rule import Rule
import arbi_agent.model.generalized_list_factory as GLFactory
import arbi_agent.model.rule.condition.condition_factory as ConditionFactory
import arbi_agent.model.rule.action.action_factory as ActionFactory


def find_delimiter_index(gl_rule):
    index = -1
    for i in range(gl_rule.get_expression_size()):
        expression = gl_rule.get_expression(i)
        if expression.is_value():
            value = expression.as_value().string_value()
            if value == "-->":
                index = i
                break
    
    return index


def new_rule_from_rule_string(subscriber, rule):
    gl = GLFactory.new_gl_from_gl_string(rule)
    return new_rule_from_gl(subscriber, gl)


def new_rule_from_gl(subscriber, gl_rule):
    if gl_rule.get_name() != 'rule':
        return None

    delimiter_index = find_delimiter_index(gl_rule)

    if delimiter_index == -1:
        return None

    conditions = []

    for i in range(delimiter_index):
        condition_expression = gl_rule.get_expression(i)

        if condition_expression.is_generalized_list() is False:
            return None

        condition = ConditionFactory.new_condition_from_gl(condition_expression.as_generalized_list())
        if condition == None:
            return None

        conditions.append(condition)

    actions = []

    for i in range(gl_rule.get_expression_size() - delimiter_index - 1):
        action_expression = gl_rule.get_expression(delimiter_index + i + 1)

        if action_expression.is_generalized_list() is False:
            return None

        action = ActionFactory.new_action_from_gl(subscriber, action_expression.as_generalized_list())
        if action == None:
            return None

        actions.append(action)

    return Rule(conditions, actions)