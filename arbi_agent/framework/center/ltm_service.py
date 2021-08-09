import redis

from arbi_agent.configuration import RedisConstants
from arbi_agent.framework.center.redis_subscriber import RedisSubscriber
from arbi_agent.framework.center.predicate_container import PredicateContainer
import arbi_agent.framework.center.redis_util as RedisUtils
import arbi_agent.model.generalized_list_factory as GLFactory
import arbi_agent.model.rule.rule_factory as RuleFactory


class LTMService:
    redis_client = redis.StrictRedis(
        host='localhost',
        port=6379,
        db=0
    )

    print("redis flushed")
    redis_client.flushdb()

    redis_pubsub = redis_client.pubsub()

    redis_subscriber = RedisSubscriber(redis_client, redis_pubsub)

    @classmethod
    def set_notification_handler(cls, handler):
        cls.redis_subscriber.set_notification_handler(handler)

    @classmethod
    def match(cls, author, fact):
        predicate = PredicateContainer(author=author, predicate=fact)
        queried = RedisUtils.query_match_data(predicate, cls.redis_client)
        if queried is not None:
            return_message = "(bind"
            binding = predicate.get_predicate().unify(queried.get_predicate(), None)
            for var in binding.get_bounded_variable_names():
                return_message += " (%s %s)" % (var, binding.retrieve(var))
            return_message += ")"
            return return_message
        else:
            return "(fail)"

    @classmethod
    def retrieve_fact(cls, author, fact):
        predicate = PredicateContainer(author=author, predicate=fact)
        queried = RedisUtils.query_match_data(predicate, cls.redis_client)
        if queried is not None:
            return str(queried.get_predicate())
        else:
            return "(fail)"

    @classmethod
    def retract_fact(cls, author, fact):
        predicate = PredicateContainer(author=author, predicate=fact)
        queried = RedisUtils.query_match_data(predicate, cls.redis_client)
        if queried is not None:
            RedisUtils.retract_data(queried, cls.redis_client)
        return "(ok)"

    @classmethod
    def update_fact(cls, author, fact):
        update_gl = GLFactory.new_gl_from_gl_string(fact)
        before = PredicateContainer(author=author, predicate=update_gl.get_expression(0).as_generalized_list())
        after = PredicateContainer(author=author, predicate=update_gl.get_expression(1).as_generalized_list())
        queried = RedisUtils.query_match_data(before, cls.redis_client)
        binding = queried.get_predicate().unify(before.get_predicate(), None)
        after = PredicateContainer(author=author, predicate=after.get_predicate().evaluate(binding))
        RedisUtils.retract_data(queried, cls.redis_client)
        RedisUtils.assert_data(after, cls.redis_client)
        cls.redis_client.publish(RedisConstants.SUBSCRIBE_CHANNEL, "(fact %s)" % str(after.get_predicate()))
        return "(ok)"

    @classmethod
    def assert_fact(cls, author, string):
        predicate = PredicateContainer(author=author, predicate=string)

        RedisUtils.assert_data(predicate, cls.redis_client)

        cls.redis_client.publish(RedisConstants.SUBSCRIBE_CHANNEL,
                                 "(fact %s)" % str(predicate.get_predicate()))

        return "(ok)"

    @classmethod
    def subscribe(cls, author, rule):
        print("author :", author)
        print("rule :", rule)
        rule = RuleFactory.new_rule_from_rule_string(author, rule)
        id = cls.redis_subscriber.add_rule(rule)
        return id

    @classmethod
    def unsubscribe(cls, author, id):
        cls.redis_subscriber.remove_rule(id)
        return "(ok)"

# import redis
# from arbi_agent.configuration import RedisConstants
# from arbi_agent.framework.center.redis_subscriber import RedisSubscriber
# from arbi_agent.framework.center.predicate_container import PredicateContainer
# import arbi_agent.framework.center.redis_util as RedisUtils
# import arbi_agent.model.generalized_list_factory as GLFactory
# import arbi_agent.model.rule.rule_factory as RuleFactory


# redis_client = redis.StrictRedis(
#     host = 'localhost',
#     port = 6379,
#     db = 0
# )
# redis_pubsub = redis_client.pubsub()

# redis_subscriber = RedisSubscriber(redis_client, redis_pubsub)

# def match(self, author, fact):
#     predicate = PredicateContainer(author = author, predicate = fact)
#     queried = RedisUtils.query_match_data(predicate, redis_client)
#     if queried != None:
#         return_message = "(bind"
#         binding = predicate.get_predicate().unify(queried.get_predicate(), None)
#         for var in binding.get_bounded_variable_names():
#             return_message += " (%s %s)" % (var, binding.retrieve(var))
#         return_message += ")"
#         return return_message
#     else:
#         return "(fail)"

# def retrieve_fact(self, author, fact):
#     predicate = PredicateContainer(author = author, predicate = fact)
#     queried = RedisUtils.query_match_data(predicate, redis_client)
#     if queried != None:
#         return str(queried.get_predicate())
#     else:
#         return "(fail)"

# def retract_fact(self, author, fact):
#     predicate = PredicateContainer(author = author, predicate = fact)
#     queried = RedisUtils.query_match_data(predicate, redis_client)
#     if queried != None:
#         RedisUtils.retract_data(queried, redis_client)
#     return "(ok)"

# def update_fact(self, author, fact):
#     update_gl = GLFactory.new_gl_from_gl_string(fact)
#     before = PredicateContainer(author = author, predicate = update_gl.get_expression(0).as_generalized_list())
#     after = PredicateContainer(author = author, predicate = update_gl.get_expression(1).as_generalized_list())
#     queried = RedisUtils.query_match_data(before, redis_client)
#     binding = queried.get_predicate().unify(before.get_predicate(), None)
#     after = PredicateContainer(author = author, predicate = after.get_predicate().evaluate(binding))
#     RedisUtils.retract_data(queried, redis_client)
#     RedisUtils.assert_data(after, redis_client)
#     redis_client.publish(RedisConstants.SUBSCRIBE_CHANNEL, 
#         "(fact %s)" % str(after.get_predicate())
#     )
#     return "(ok)"

# def assert_fact(self, author, string):
#     predicate = PredicateContainer(author = author, predicate = string)
#     RedisUtils.assert_data(predicate, redis_client)
#     redis_client.publish(RedisConstants.SUBSCRIBE_CHANNEL, 
#         "(fact %s)" % str(predicate.get_predicate())
#     )

# def subscribe(self, author, rule):
#     rule = RuleFactory.new_rule_from_rule_string(author, rule)
#     id = redis_subscriber.add_rule(rule)
#     return id

# def unsubscribe(self, author, id):
#     redis_subscriber.remove_rule(id)
#     return "(ok)"
