# -*- coding: utf-8 -*-
import itchat
from itchat.content import *
from HistoryRecorder import HistoryRecorder
from GroupTagCloud import GroupTagCloud
from ActivityInfo import ActivityInfo
from ProcessInterface import ProcessInterface
from QAPlugin import QAPlugin
from LastSpeakTime import LastSpeakTime

import logging
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

# Some global switches for debugging use only
isDebug = not True

itchat.auto_login(True)
plugins = [
    #GlobalTextHook({ '^ding$': 'dong', '小明': '嘎？' }),
    #PaiDuiHook(),
    HistoryRecorder(),
    GroupTagCloud(),
    ActivityInfo(),
    QAPlugin(onlyOwerUse = True),
    LastSpeakTime(),
    #GroupMessageForwarder([ '二群', '三群' ], [ 'AI二群测试中', 'AI三群测试' ])
]
for plugin in plugins:
    if not isinstance(plugin, ProcessInterface):
        logging.error('One of the plugins are not a subclass of ProcessInterface.')
        exit(-1)

@itchat.msg_register([TEXT], isGroupChat=True)
def text_reply(msg):
    if isDebug:
        logging.info(msg)
    for plugin in plugins:
        try:
            plugin.process(msg, TEXT)
        except Exception as e:
            logging.error(e) # so that one plug's failure won't prevent others from being executed

if __name__ == '__main__':
    itchat.run()
