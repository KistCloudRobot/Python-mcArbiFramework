from abc import *

class Condition(metaclass = ABCMeta) :

    @abstractmethod
    def check_condition(self) :
        pass

    @abstractmethod
    def get_predicate_name(self) :
        pass
    
    @abstractmethod
    def get_expressions(self, binding) :
        pass