from ProcessInterface import ProcessInterface
from itchat.content import *
from pymongo import MongoClient, DESCENDING
from utilities import *
import itchat
import tablib
import re

# class lastRecord():
#     name = ''
#     content = ''
#     timestamp = -1
#     rtime = None
#     def __init__(self, name, content, rtime, timestamp = -1):
#         self.name = name
#         self.content = content
#         self.rtime = rtime
#         self.timestamp = timestamp

class LastSpeakTime(ProcessInterface):
    def __init__(self):
        # self.coll = DbClient[dbName][collName]
        self.fileName = 'lastRecord.xlsx'
        pass

    def process(self, msg, type):
        # if not OnOffs[PluginName.Last]:
        #     return

        if type != TEXT:
            return

        if msg['Content'] != '/last':
            return

        group_id, group_name = get_group_info(msg)
        room = itchat.update_chatroom(group_id, detailedMember=True)

        # ower = room['MemberList'][0]['UserName']
        # if msg['ActualUserName'] != ower:
        #     return

        records = []
        for p in room['MemberList']:
            timestamp = -1
            content = ''
            rtime = ''
            name = p['DisplayName'] if p['DisplayName'] != '' else p['NickName']
            record = list(HisColl.find({'to': group_name, 'from': name}).sort([('timestamp', DESCENDING)]).limit(1))
            if len(record) != 0:
                try:
                    record = record[0]
                    timestamp = record['timestamp']
                    content = record['content']
                    rtime = record['time']
                except Exception as e:
                    logging.error(e)

            records.append((name, content, rtime, timestamp))

        records = sorted(records, key=lambda rr: rr[3])
        header = (u'昵称', u'最后发言时间', u'内容')
        mylist = []
        for r in records:
            mylist.append((r[0], r[2], r[1]))
        mylist = tablib.Dataset(*mylist, headers=header)
        with open(self.fileName, 'wb') as f:
            f.write(mylist.xlsx)

        itchat.send_file(self.fileName, group_id)
