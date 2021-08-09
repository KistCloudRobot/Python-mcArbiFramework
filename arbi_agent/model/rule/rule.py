import copy

class Rule() :

    def __init__(self, conditions, actions) :
        self.conditions = copy.deepcopy(conditions)
        self.actions = copy.deepcopy(actions)

    def get_conditions(self) :
        return self.conditions

    def get_actions(self) :
        return self.actions