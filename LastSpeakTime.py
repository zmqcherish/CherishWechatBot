from ProcessInterface import ProcessInterface
from itchat.content import *
from pymongo import MongoClient, DESCENDING
from utilities import *
import itchat
import tablib

class lastRecord():
    name = ''
    content = ''
    timestamp = -1
    rtime = None
    def __init__(self, name, content, rtime, timestamp = -1):
        self.name = name
        self.content = content
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
            name = p['NickName']
            record = list(self.coll.find({'to': groupName, 'from': name}).sort({timestamp: 1}).limit(1))
            if len(record) == 0:
                timestamp = -1
                content = ''
                rtime = None
            else:
                record = record[0]
                timestamp = record['timestamp']
                content = record['content']
                rtime = record['time']
            records.append(lastRecord(name, content, rtime, timestamp))

        sorted(records, key=lambda r: r.timestamp, reverse=True)
        header = (u'昵称', u'最后发言时间', u'内容')
        mylist = []
        for r in records:
            mylist.append((r.name, r.rtime, r.content))
        mylist = tablib.Dataset(*mylist, headers=header)
        with open('1.xlsx', 'wb') as f:
            f.write(mylist.xlsx)
        a =1
       # records = self.coll.find({'to': groupName}).sort([('timestamp', DESCENDING)]).limit(self.recordMaxNum)





