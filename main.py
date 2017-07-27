# -*- coding: utf-8 -*-
from itchat.content import *
from HistoryRecorder import HistoryRecorder
from GroupTagCloud import GroupTagCloud
from ActivityInfo import ActivityInfo
from ProcessInterface import ProcessInterface
from QAPlugin import QAPlugin
from LastSpeakTime import LastSpeakTime
from MemberDistribution import MemberDistribution
from PrivateChat import PrivateChat
from SysReminder import SysReminder
from Tuling import Tuling
from KeyHandler import KeyHandler
from BotSetting import BotSetting
from MsDuilian import MsDuilian
from MicoIce import MicoIce
from BingText2Speech import BingText2Speech
from ChengYuJieLong import ChengYuJieLong
# from VSGame import VSGame
from LrcCreator import LrcCreator
from EasterEgg import EasterEgg
from utilities import *
import shutil
import logging
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

# Some global switches for debugging use only
isDebug = False

itchat.auto_login(True, enableCmdQR=2)

settingPlugin = BotSetting()        # 机器人设置
privateChatPlugin = PrivateChat()   # 私聊调用 tuling
sysReminderPlugin = SysReminder()   # 红包 新成员 撤回
historyPlugin = HistoryRecorder()   # 记录消息
plugins = [
    #PaiDuiHook(),
    KeyHandler(),
    GroupTagCloud(),
    ActivityInfo(),
    QAPlugin(),
    LastSpeakTime(),
    MemberDistribution(),
    Tuling(),
    MsDuilian(),
    BingText2Speech(),
    ChengYuJieLong(),
    LrcCreator(),
    EasterEgg(),
    # VSGame(),
    MicoIce(),
    #GroupMessageForwarder([ '二群', '三群' ], [ 'AI二群测试中', 'AI三群测试' ])
]
for plugin in plugins:
    if not isinstance(plugin, ProcessInterface):
        logging.error('One of the plugins are not a subclass of ProcessInterface.')
        exit(-1)

#群消息 文本和图片
@itchat.msg_register([TEXT,PICTURE,VOICE], isGroupChat=True)
def text_reply(msg):
    historyPlugin.process(msg, msg['Type'])
    settingPlugin.process(msg, TEXT)    #设置
    if not isRun(msg):
        return
    for plugin in plugins:
        try:
            plugin.process(msg, msg['Type'])
        except Exception as e:
            logging.error('{}:{}'.format(e, str(type(plugin))))  # so that one plug's failure won't prevent others from being executed

#私聊调用图灵机器人
@itchat.msg_register([TEXT,VOICE], isFriendChat=True)
def text_reply(msg):
    if not isRun(msg):
        return
    try:
        historyPlugin.process2(msg, msg['Type'])
        privateChatPlugin.process(msg, TEXT)
    except Exception as e:
        logging.error(e)

#系统消息：红包 新成员 撤回
@itchat.msg_register([NOTE], isGroupChat=True)
def text_reply(msg):
    if not isRun(msg):
        return
    try:
        sysReminderPlugin.process(msg, NOTE)
    except Exception as e:
        logging.error(e)

#小冰
@itchat.msg_register([TEXT,SYSTEM,PICTURE,VOICE], isMpChat=True)
def xiaoice_replay(msg):
    if not isRun(msg):
        return
    try:
        plugins[-1].process(msg, msg['Type'])    #小冰
    except Exception as e:
        logging.error(e)

# @itchat.msg_register([FRIENDS,SYSTEM,NOTE])
# def add_friend(msg):
#     # return
#     itchat.add_friend(msg['FromUserName']) # 该操作会自动将新好友的消息录入，不需要重载通讯录
    # itchat.send_msg('Nice to meet you!', msg['FromUserName'])

#软件是否调试模式 是否响应用户指令
def isRun(msg):
    if isDebug:
        logging.info(msg)

    # if isBlock(msg):
    #     logging.info('黑名单群...')
    #     return False

    if Settings[SettingEnum.MainOnOff]:
        return True

    logging.info('机器人已关闭')
    historyPlugin.process(msg, msg['Type']) #依然记录消息
    return False

def bot_init():
    # bingPath = 'Bing'
    # if not os.path.exists(bingPath):
    #     os.mkdir(bingPath)

    paths = ['ChatImg', 'Temp']
    for path in paths:
        if os.path.exists(path):
            shutil.rmtree(path) #先清空
        os.mkdir(path)

if __name__ == '__main__':
    bot_init()
    itchat.run()
