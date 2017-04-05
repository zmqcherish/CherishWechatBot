from ProcessInterface import ProcessInterface
from itchat.content import *
from pymongo import MongoClient, DESCENDING
from utilities import *
import itchat

class lastRecord():
    pId = ''
    name = ''
    timestamp = -1
    rtime = None
    def __init__(self,pId,name,rtime,timestamp = -1):
        self.pId = pId
        self.name = name
        self.rtime = rtime
        self.timestamp = timestamp

    def __cmp__(self, other):
        if self.timestamp == other.timestamp:
            return 0
        elif self.timestamp > other.timestamp:
            return 1
        else:
            return -1

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

        groupName = msg['User']['NickName']
        roomId = getChatroomIdByName([groupName])
        if roomId is None:
            return
        room = itchat.update_chatroom(roomId[0], detailedMember=True)
        records = []
        for p in room['MemberList']:
            pId = p['UserName']
            record = list(self.coll.find({'to': groupName, 'fromId': pId}).sort([('timestamp', DESCENDING)]).limit(1))
            if len(record) == 0:
                timestamp = -1
                name = msg['NickName']
                rtime = None
            else:
                record = record[0]
                timestamp = record['timestamp']
                name = record['from']
                rtime = record['time']
            records.append(lastRecord(pId, name, rtime, timestamp))

        sorted(records, key=lambda r: r.timestamp, reverse=True)
        a =1
       # records = self.coll.find({'to': groupName}).sort([('timestamp', DESCENDING)]).limit(self.recordMaxNum)





