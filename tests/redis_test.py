import redis
import threading
import time

def test() :
    redis_client = redis.StrictRedis(host = 'localhost', port = 6379, db = 0)

    redis_pubsub = redis_client.pubsub()

    redis_pubsub.subscribe('LTMSubscribe')

    threading.Thread(target=redis_listener, args=(redis_pubsub,)).start()

    time.sleep(1)

    redis_client.publish("LTMSubscribe", "(test)")

def redis_listener(redis_pubsub : redis.client.PubSub) :

    while True :
        for message in redis_pubsub.listen() :
            print("redis message arrived : ")
            print(message)

    

if __name__ == "__main__":
    test()