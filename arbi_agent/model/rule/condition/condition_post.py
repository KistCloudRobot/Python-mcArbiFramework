from arbi_agent.model.rule.condition.condition import Condition

class PostCondition(Condition) :

    def __init__(self, gl) :
        pass

    def check_condition(self) :
        return False

    def get_predicate_name(self) :
        return None

    def get_expressions(self) :
        return None