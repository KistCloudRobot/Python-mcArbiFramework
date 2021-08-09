import json
import threading
import time

from multimethod import multimethod

def dict_test() :
    data = {}
    data["test1"] = "test1"
    data["test2"] = "test2"

    json_string = json.dumps(data)

    print(json_string)

    print(json.loads(json_string))


def lock_test(lock, test_number) :
    with lock :
        print("hello! : " + str(test_number))
        time.sleep(3)

class test_class() :
    test_var = 42
    print("this line work only once")

    def __init__(self, var) :
        print("class init")
        self.test_var2 = var

    def test_method(self) :
        print(test_class.test_var)
        print(self.test_var2)


def arg_test(index, *test_args) :
    print(test_args)
    print(test_args.__len__())
    print(test_args[index])

@multimethod
def same_name_function(arg:int) :
    print("method 1")
    print(str(arg))

@multimethod
def same_name_function(arg:str) :
    print("method 2")
    print(arg)

def escape(content) :
    string = ""

    index = 0

    for i in content :
        if i == "<" :
            string = string + "&lt;"
        elif i == ">" :
            string = string + "&gt;"
        elif i == "&" :
            string = string + "&amp;"
        elif i == '"' :
            string = string + "&quot;"
        elif i == "'" :
            string = string + "&apos;"
        else:
            string = string + i

        index = index + 1

    return string

if __name__ == "__main__":
    # dict_test()

    # lock = threading.Lock()

    # t1 = threading.Thread(target=lock_test, args=(lock, 1))
    # t2 = threading.Thread(target=lock_test, args=(lock, 2))

    # t1.start()
    # t2.start()

    # obj1 = test_class(1)
    # obj2 = test_class(2)

    # obj1.test_method()
    # obj2.test_method()

    # print("dkdkd")
    # same_name_function(10)
    # same_name_function("test")

    # test_argu = 1,2,3,4

    # arg_test(0, *())

    # print( 'abc' > 'cfd' )

    test_list = []

    test_tup = (1,2,3,4)

    print(test_tup.__len__())

    for integer in test_tup :
        print(integer)