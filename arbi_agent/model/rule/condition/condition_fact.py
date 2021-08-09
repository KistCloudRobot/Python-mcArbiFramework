from arbi_agent.model.rule.condition.condition import Condition

class FactCondition(Condition) :

    def __init__(self, predicate) :
        self.predicate = predicate

    def check_condition(self) :
        return False

    def get_predicate_name(self) :
        return self.predicate.get_name()

    def get_expressions(self) :
        exps = []
        for i in range(self.predicate.get_expression_size()) :
            exps.append(self.predicate.get_expression(i))
        return exps

    def __str__(self) :
        return str(self.predicate) 