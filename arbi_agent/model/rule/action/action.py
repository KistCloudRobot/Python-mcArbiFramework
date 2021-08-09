from abc import *

class Action(metaclass = ABCMeta) :

    @abstractmethod
    def get_subscriber(self) :
        pass

    @abstractmethod
    def to_action_content(self) :
        pass
    
    @abstractmethod
    def bind(self, binding) :
        pass