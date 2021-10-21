import os
from datetime import datetime
from ProcessInterface import ProcessInterface
from itchat.content import *
from util import *


class HistoryRecorder(ProcessInterface):
    def __init__(self):
        self.imgDir = 'ChatImg'

    def process(self, msg, type):
        group_id, group_name = get_group_info(msg)

        if group_name not in save_group:
            return

        content = msg['Content']
        # if type == SYSTEM:
        #     coll = SysColl
        #
        # else: #TEXT PICTURE VOICE
        #     coll = HisColl
        if type == PICTURE or type == VOICE:
            fn = msg['FileName']
            new_fn = os.path.join(self.imgDir, fn)
            msg['Text'](fn)
            os.rename(fn, new_fn)
            content = new_fn

        insert_msg((msg['MsgId'], type, content, msg['ActualNickName'], msg['ActualUserName'], msg['ToUserName'], group_name, time(), datetime.now(time_zone).strftime('%Y-%m-%d %H:%M:%S')))

        # if group_name not in NotEchoGroup:
        logging.info('{}-{}:{}\n'.format(group_name, msg['ActualNickName'], content))

    # def process2(self, msg, type):
    #     person = msg['User']['NickName']
    #     if person != '大萌📸':
    #         return
    #     content = msg['Content']
    #     rtime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    #
    #     if type == VOICE:
    #         fn = msg['FileName']
    #         newfn = os.path.join('person', rtime)
    #         msg['Text'](fn)
    #         os.rename(fn, newfn)
    #         content = newfn
    #
    #     timestamp = time()
    #
    #     r = {
    #         'msgId': msg['MsgId'],
    #         'content': content,
    #         'from': person,
    #         'fromId': msg['FromUserName'],
    #         'alias': msg['User']['Alias'],
    #         'timestamp': timestamp,
    #         'time': rtime
    #     }
    #     FriendColl.insert(r)
