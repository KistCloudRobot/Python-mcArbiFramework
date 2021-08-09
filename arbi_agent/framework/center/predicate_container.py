import arbi_agent.model.generalized_list_factory as GLFactory
from arbi_agent.model.generalized_list import GeneralizedList
import time


class PredicateContainer:
    def __init__(self, **kwds):

        if ('author' not in kwds
                or 'predicate' not in kwds
        ):
            return

        self.author = kwds['author']

        if 'create_time' not in kwds:
            self.create_time = str(time.time() % 1)[2:8]
        else:
            self.create_time = kwds['create_time']

        predicate = kwds['predicate']

        if type(predicate) == str:
            self.predicate = GLFactory.new_gl_from_gl_string(predicate)
        elif type(predicate) == GeneralizedList:
            self.predicate = predicate

    def get_author(self):
        return self.author

    def get_create_time(self):
        return self.create_time

    def get_predicate(self):
        return self.predicate
