from abc import ABCMeta


class ActionBody(metaclass=ABCMeta):
    def excute(self, obj) -> object:
        pass
