from enum import Enum


class BrokerType(Enum):
    ZERO_MQ = 0
    MC = 1


class ServerLauncherConstants:
    BROKER_PORT = 61616
    BROKER_HOST = "127.0.0.1"
    BROKER_NAME = "centerBroker"
    BROKER_TYPE = BrokerType.ZERO_MQ
    DEFAULT_CONFIGURATION_LOCATION = "../configuration/ServerConfiguration.xml"


class LoggerContents:
    INTERACTION_MANAGER_ADDRESS = "agent://www.arbi.com/interactionManager"


class AgentConstants:
    TOOLKIT_THREAD_NUMBER = 20


class AgentMessageAction(Enum):
    RequestStream = 0
    Push = 1
    ReleaseStream = 2
    Request = 3
    Query = 4
    Inform = 5
    Response = 6
    Subscribe = 7
    Unsubscribe = 8
    Notify = 9
    System = 10

class LTMConstants:
    TOOLKIT_THREAD_NUMBER = 20

class LTMMessageAction(Enum):
    RequestStream = 0
    Push = 1
    RelaseStream = 2
    AssertFact = 3
    RetrieveFact = 4
    UpdateFact = 5
    RetractFact = 6
    Match = 7
    Result = 8
    Subscribe = 9
    Unsubscribe = 10
    Notify = 11
    GetLastModifiedTime = 12


class GLValueType:
    TYPE_INT = "INT"
    TYPE_FLOAT = "FLOAT"
    TYPE_STRING = "STRING"
    TYPE_UNDIFINED = "UNDIFINED"


class RedisConstants:
    SUBSCRIBE_CHANNEL = 'LTMSubscribe'
    PREDICATE_PREFIX = 'predicate:'
    PREDICATE_NAME_PREFIX = 'predicateName:'
    CREATE_TIME_KEY = 'CreateTime'
    PREDICATE_NAME_KEY = 'Predicate'
    AUTHOR_KEY = "Author"
    EXPRESSION_NUMBER_KEY = "ExpressionNumber"
    EXPRESSION_PREFIX = "Expression:"


class ConditionType:
    TYPE_FACT = 'fact'
    TYPE_EXPRESSION = 'expression'
    TYPE_POST = 'post'
    TYPE_EVENT = 'event'
    TYPE_RETRACT = 'retracted'


class ActionType:
    TYPE_NOTIFY = 'notify'
    TYPE_STEAM = 'stream'
