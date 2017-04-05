from itchat.content import *
from utilities import *
from ProcessInterface import ProcessInterface
from pymongo import MongoClient
from datetime import datetime
import itchat
import re

class QAPlugin(ProcessInterface):
    def __init__(self, onlyOwerUse = False):
        self.client = MongoClient()
        self.collName = 'QA'
        self.coll = self.client[dbName][self.collName]
        self.onlyOwerUse = onlyOwerUse
        logging.info('QAPlugin initialized.')

    def process(self, msg, type):
        if type != TEXT:
            return

        content = msg['Content']
        destinationChatroomId = msg['FromUserName'] if re.search('@@', msg['FromUserName']) else msg['ToUserName']
        if content.startswith('/qa '):

            BlockChatRoomIds = None
            #BlockChatRoomIds = getChatroomIdByName([u'知乎最牛逼兄弟会没有之一'])

            if (BlockChatRoomIds is not None) and (destinationChatroomId in BlockChatRoomIds):
                return

            qa = content.split()
            if len(qa) == 3:
                question = qa[1]
                answer = qa[2]

                SpecialChatRoomIds = getChatroomIdByName(['qqq', u'知乎最牛逼兄弟会没有之一'])
                if (SpecialChatRoomIds is not None) and (destinationChatroomId in SpecialChatRoomIds):
                    if self.onlyOwerUse:
                        if 'ChatRoomOwner' in msg['User']:
                            ower = msg['User']['ChatRoomOwner']
                        else:
                            ower = msg['User']['MemberList'][0]['UserName']
                        if msg['ActualUserName'] != ower:
                            itchat.send(u'我只听群主的话！', destinationChatroomId)
                            return

                #destinationChatroomId = msg['FromUserName'] if re.search('@@', msg['FromUserName']) else msg['ToUserName']
                res = list(self.coll.find({'question': question, 'to': msg['User']['NickName']}))
                if len(res) == 1:
                    itchat.send(u'我知道答案，不用你教我~', destinationChatroomId)
                else:
                    timestamp = time()
                    rtime = datetime.utcfromtimestamp(timestamp)
                    r = {
                        'question': question,
                        'answer': answer,
                        'from': msg['ActualNickName'],
                        'fromId': msg['ToUserName'],
                        'to': msg['User']['NickName'] if 'User' in msg and 'UserName' in msg['User'] else 'N/A',
                        'timestamp': timestamp,
                        'time': rtime
                    }
                    self.coll.insert(r)
                    itchat.send(u'so easy! 我记住了，不信你考我！', destinationChatroomId)
                    logging.info('QA remember:{0}:{1}'.format(question, answer))
        else:
            res = list(self.coll.find({'question': content, 'to': msg['User']['NickName']}))
            if len(res) == 1:
                itchat.send(res[0]['answer'], destinationChatroomId)
