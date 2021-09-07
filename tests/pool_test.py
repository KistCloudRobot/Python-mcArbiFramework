import time
from multiprocessing import Pool
from multiprocessing.pool import ThreadPool
from threading import Thread


def test(arg):
    print('shart!', arg)
    time.sleep(5)
    print('finish!', arg)


class TestClass:
    def __init__(self):
        self.pool = ThreadPool(processes=5)

    def test(arg):
        print('shart!', arg)
        time.sleep(5)
        print('finish!', arg)

    def start(self):
        i = 0
        while True:
            self.run(i)
            i = i + 1


    def run(self, arg):
        self.pool.apply_async(test, args=(arg, ))




if __name__ == '__main__':
    testClass = TestClass()
    Thread(target=testClass.start, args=(), daemon=True).start()
    input()
