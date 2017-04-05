from ProcessInterface import ProcessInterface
from itchat.content import *
from pymongo import MongoClient
from utilities import *

class LastSpeakTime(ProcessInterface):
    def __init__(self):
        self.client = MongoClient()
        self.coll = self.client[dbName][collName]
        pass

    def process(self, msg, type):
        if type != TEXT:
            return

        if msg['Content'] != '/last':
            return

