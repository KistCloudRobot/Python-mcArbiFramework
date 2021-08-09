from arbi_agent.configuration import RedisConstants
import redis
import sys
from arbi_agent.model.expression.expression_list import ExpressionList
from arbi_agent.model.expression.expression_generalized_list import GLExpression
from arbi_agent.model.expression.expression_value import ValueExpression
from arbi_agent.model.value.value_string import StringValue
from arbi_agent.framework.center.predicate_container import PredicateContainer
from arbi_agent.model import generalized_list_factory as GLFactory


def query_predicate_data_by_key(key, redis_client: redis.StrictRedis):
    if key.startswith(RedisConstants.PREDICATE_PREFIX) is not True:
        key = '%s%s' % (RedisConstants.PREDICATE_PREFIX, key)

    size = int(redis_client.hget(key, RedisConstants.EXPRESSION_NUMBER_KEY))
    exps = ExpressionList()

    for i in range(size):
        expression = redis_client.hget(key, RedisConstants.EXPRESSION_PREFIX + str(i)).decode('utf-8')

        if expression.startswith(RedisConstants.PREDICATE_PREFIX):
            exps.add(GLExpression(query_predicate_data_by_key(expression, redis_client).get_predicate()))
        else:
            exps.add(ValueExpression(StringValue(expression)))

    predicate = GLFactory.new_generalized_list(
        redis_client.hget(key, RedisConstants.PREDICATE_NAME_KEY).decode('utf-8'),
        *(exps.get_expression_list()))

    print(predicate)

    return PredicateContainer(
        author=redis_client.hget(key, RedisConstants.AUTHOR_KEY).decode('utf-8'),
        create_time=int(redis_client.hget(key, RedisConstants.CREATE_TIME_KEY)),
        predicate=predicate)


def query_match_data(predicate, redis_client: redis.StrictRedis):
    name = predicate.get_predicate().get_name()
    predicate_key_list = redis_client.zrange(RedisConstants.PREDICATE_NAME_PREFIX + name, 0, -1)

    for i in range(len(predicate_key_list)):
        queried_gl = query_predicate_data_by_key(predicate_key_list[i].decode('utf-8'), redis_client)
        binding = predicate.get_predicate().unify(queried_gl.get_predicate(), None)
        if binding is not None:
            print("qgl : " + str(queried_gl.get_predicate()))
            return queried_gl

    return None


def retract_gl(create_time, predicate, redis_client: redis.StrictRedis):
    for i in range(predicate.get_expression_size()):
        if predicate.get_expression(i).is_generalized_list():
            retract_gl(create_time, predicate.get_expression(i).as_generalized_list, redis_client)
        key = make_predicate_key(predicate.get_name(), create_time)
        print('retract key : ' + key)
        redis_client.delete(key)


def retract_data(queried, redis_client: redis.StrictRedis):
    if queried is None:
        return
    retract_gl(queried.get_create_time(), queried.get_predicate(), redis_client)
    redis_client.zrem(
        '%s%s' % (RedisConstants.PREDICATE_NAME_PREFIX, queried.get_predicate().get_name()),
        make_predicate_key(queried.get_predicate().get_name(), queried.get_create_time())
    )


def assert_gl(author, create_time, predicate, redis_client: redis.StrictRedis):
    key = make_predicate_key(predicate.get_name(), create_time)

    print("redis util assert gl: predicate: " + str(predicate))

    redis_client.hset(key, RedisConstants.AUTHOR_KEY, author)
    redis_client.hset(key, RedisConstants.CREATE_TIME_KEY, str(create_time))
    redis_client.hset(key, RedisConstants.PREDICATE_NAME_KEY, predicate.get_name())
    redis_client.hset(key, RedisConstants.EXPRESSION_NUMBER_KEY, str(predicate.get_expression_size()))

    for i in range(predicate.get_expression_size()):
        if predicate.get_expression(i).is_generalized_list():
            subkey = assert_gl(author, create_time, predicate.get_expression(i).as_generalized_list(), redis_client)
            redis_client.hset(key, RedisConstants.EXPRESSION_PREFIX + str(i), subkey)
        else:
            redis_client.hset(key, RedisConstants.EXPRESSION_PREFIX + str(i),
                              str(predicate.get_expression(i)).replace("\"", ""))
    return key


def assert_data(data, redis_client: redis.StrictRedis):
    key = assert_gl(data.get_author(), data.get_create_time(), data.get_predicate(), redis_client)
    print("assert result key : " + key)

    redis_client.zadd(
        '%s%s' % (RedisConstants.PREDICATE_NAME_PREFIX, data.get_predicate().get_name()),
        {make_predicate_key(data.get_predicate().get_name(), data.get_create_time()): sys.maxsize - int(
            data.get_create_time())}
    )


def make_predicate_key(name, time):
    return '%s%s:%s' % (RedisConstants.PREDICATE_PREFIX, name, str(time))
