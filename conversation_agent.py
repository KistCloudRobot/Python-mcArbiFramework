# -*- coding: utf-8 -*-
# import json

import threading
from time import sleep
from arbi_agent.agent.arbi_agent import ArbiAgent
from arbi_agent.configuration import BrokerType
import arbi_agent.model.parser.gl_parser_implementation as GLParser

from arbi_agent.ltm.data_source import DataSource


class ConversationAgent(ArbiAgent):
    def __init__(self, data_source: DataSource):
        self.listenT = threading.Thread(target=self.listen)
        self.listenT.daemon = True
        self.data_source = data_source

    def listen(self):
        while True:
            R = sr.Recognizer()
            with sr.Microphone() as source:
                print(source.list_microphone_names())
                print("Say Something!")
                R.adjust_for_ambient_noise(source)
                AUDIO = R.listen(source, phrase_time_limit=10)
                
            f = open("e:\\authentication\\Test Project-6e4fe23cb9a7.json", "r")
            try:
                TXT = R.recognize_google_cloud(AUDIO, credentials_json=f.read(), language="ko-KR")
                print("Google Cloud Result " + TXT)
                self.data_source.assert_fact('(VoiceReceived "' + TXT + '")')
                return
            except sr.UnknownValueError:
                print("Can't understand audio.")
                continue
            except sr.RequestError as e:
                print(e)
                raise e

    def on_request(self, sender, data):
        data_gl = GLParser.parse_generalized_list(data)
        print(data_gl.get_name())
        if self.listenT.isAlive():
            return "(error \"AlreadyListening\")"

        self.listenT.start()
        return "(ok)"
        

class ConversationDataSource(DataSource):
    def on_notify(self, content):
        print("notification arrived")
        print(content)


if __name__ == "__main__":

    sleep(1)

    print("agent ready")

    ds = ConversationDataSource()
    ds.connect("tcp://172.16.165.124:61616", "ds://conversation_ds", BrokerType.TYPE_ZERO)

    agent = ConversationAgent(ds)
    agent.initialize(agent_url="agent://conversation_agent", 
                     broker_url="tcp://172.16.165.124:61616", 
                     broker_type=BrokerType.TYPE_ZERO)
    sleep(1)

    ds.assert_fact('(TestGL "TestData")')

    print("check redis")

    # sleep(5)
    # print("retract")
    # ds.retract_fact('(TestGL "TestData")')

    # print("finish")

    # sub_id = ds.subscribe("(rule (fact (TestModel $model)) --> (notify (TestModel $model)))")

    # print(sub_id)

    # sleep(1)

    # ds.assert_fact('(TestModel "TestModel")')

    # sleep(1)

    # ds.unsubscribe(sub_id)

    # sleep(1)

    # ds.assert_fact("(TestModel \"TestModel2\")")

    # sleep(1)

    # result = ds.retrieve_fact("(TestModel $a)")

    # print(result)

    # sleep(1)

    # data = ds.match("(TestModel $a)")

    # print(data)

    # sleep(1)

    # ds.retract_fact('(TestModel "TestModel")')

    # sleep(1)

    # result = ds.retrieve_fact("(TestModel $a)")

    # print(result)

    # sleep(1)

    # ds.update_fact("(update (TestModel $a) (newTestModel $a))")

    # sleep(1)

    # result = ds.retrieve_fact("(newTestModel $a)")

    # print(result)

    sleep(1)

    while True:
        sleep(1)
