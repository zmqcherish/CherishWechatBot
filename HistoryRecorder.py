import os
from datetime import datetime
from ProcessInterface import ProcessInterface
from itchat.content import *
from utilities import *
import pytz

class HistoryRecorder(ProcessInterface):
    def __init__(self):
        self.imgDir = 'ChatImg'
        logging.info('HistoryRecorder connected to MongoDB.')

    def process(self, msg, type):
        content = msg['Content']
        if type == SYSTEM:
            coll = SysColl

        else: #TEXT PICTURE VOICE
            coll = HisColl
            if type == PICTURE or type == VOICE:
                fn = msg['FileName']
                newfn = os.path.join(self.imgDir, fn)
                msg['Text'](fn)
                os.rename(fn, newfn)
                content = newfn

        tz = pytz.timezone('Asia/Shanghai')
        group_id, group_name = get_group_info(msg)
        r = {
            'msgId': msg['MsgId'],
            'type': type,
            'content': content,
            'from': msg['ActualNickName'],
            'userName': msg['ActualUserName'],
            'fromId': msg['ToUserName'],
            'to': group_name,
            'timestamp': time(),
            'time': datetime.now(tz).strftime('%Y-%m-%d %H:%M:%S')
        }
        coll.insert(r)
        if group_name not in NotEchoGroup:
            print('{0}-{1}:{2}\n'.format(group_name, msg['ActualNickName'], content))

    def process2(self, msg, type):
        person = msg['User']['NickName']
        if person != '大萌📸':
            return
        content = msg['Content']
        rtime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        if type == VOICE:
            fn = msg['FileName']
            newfn = os.path.join('person', rtime)
            msg['Text'](fn)
            os.rename(fn, newfn)
            content = newfn

        timestamp = time()
        
        r = {
            'msgId': msg['MsgId'],
            'content': content,
            'from': person,
            'fromId': msg['FromUserName'],
            'alias': msg['User']['Alias'],
            'timestamp': timestamp,
            'time': rtime
        }
        FriendColl.insert(r)
