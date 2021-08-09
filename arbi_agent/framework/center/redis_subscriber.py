import time
import threading

from arbi_agent.configuration import RedisConstants
from arbi_agent.model import generalized_list_factory as GeneralizedListFactory
from arbi_agent.model.binding import Binding
from arbi_agent.framework.center.predicate_container import PredicateContainer
import arbi_agent.model.rule.condition.condition_factory as ConditionFactory
import arbi_agent.framework.center.redis_util as RedisUtil


class RedisSubscriber:

    def __init__(self, redis_client, redis_pubsub, ):
        self.redis_client = redis_client
        self.redis_pubsub = redis_pubsub

        self.subscribed_rules_by_predicate_name = {}
        self.subscribed_rules_by_id = {}

        self.redis_pubsub.subscribe(RedisConstants.SUBSCRIBE_CHANNEL)

        self.handler = None

        on_message_thread = threading.Thread(target=self.on_redis_message, args=())
        on_message_thread.daemon = True
        on_message_thread.start()

    def set_notification_handler(self, handler):
        self.handler = handler

    def check_subscribe_rules(self, condition):

        predicate_name = condition.get_predicate_name()

        if predicate_name not in self.subscribed_rules_by_predicate_name:
            return

        rules = self.subscribed_rules_by_predicate_name[predicate_name]

        if rules is None or len(rules) == 0:
            return
        binding = Binding()
        condition_satisfied = False
        for rule in rules:
            condition_satisfied = True
            for rule_condition in rule.get_conditions():
                temp_binding = self.evaluate(rule_condition)
                if temp_binding is not None:
                    binding.copy(temp_binding)
                else:
                    condition_satisfied = False
                    break

            if condition_satisfied:
                for action in rule.get_actions():
                    action.bind(binding)
                    self.handler.notify(action)

    def evaluate(self, condition):
        data = PredicateContainer(author=None, predicate=str(condition))
        queried_data = RedisUtil.query_match_data(data, self.redis_client)

        if queried_data is not None:
            binding = data.get_predicate().unify(queried_data.get_predicate(), None)
            return binding

        return None

    def add_rule(self, rule):
        conditions = rule.get_conditions()
        sub_id = "Subscribe:" + str(time.time() % 1)[2:8]
        for i in range(conditions.__len__()):
            # if self.subscribed_rules_by_predicate_name[conditions[i].get_predicate_name()] == None :
            if conditions[i].get_predicate_name() not in self.subscribed_rules_by_predicate_name:
                self.subscribed_rules_by_predicate_name[conditions[i].get_predicate_name()] = []
            (self.subscribed_rules_by_predicate_name[conditions[i].get_predicate_name()]).append(rule)
            pattern = self.make_pattern_string(conditions[i])
            self.redis_pubsub.psubscribe(pattern)
        self.subscribed_rules_by_id[sub_id] = rule
        return sub_id

    def make_pattern_string(self, condition):
        pattern = "(fact (%s" % condition.get_predicate_name()
        for expression in condition.get_expressions():
            pattern += " "
            if expression.is_variable():
                pattern += "*"
            else:
                pattern += str(expression)
        pattern += "))"
        return pattern

    def remove_rule(self, sub_id):
        rule = self.subscribed_rules_by_id.pop(sub_id)
        conditions = rule.get_conditions()
        for condition in conditions:
            self.subscribed_rules_by_predicate_name[condition.get_predicate_name()].remove(rule)

    def on_redis_message(self):
        while True:
            for message in self.redis_pubsub.listen():
                if type(message['data']) == int:
                    continue

                condition = ConditionFactory.new_condition_from_gl_string(message['data'].decode("utf-8"))
                self.check_subscribe_rules(condition)
