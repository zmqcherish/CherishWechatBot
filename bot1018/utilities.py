# -*- coding: utf-8 -*-
"""
Some utility functions
"""
import logging
from pymongo import MongoClient
import random
from time import time
import itchat
from enum import Enum
import os
import re
#import numpy as np
from matplotlib.font_manager import FontProperties

dbName = 'bothistory'
dbClient = MongoClient()
HisColl = dbClient[dbName]['history']
SysColl = dbClient[dbName]['syshistory']
FriendColl = dbClient[dbName]['friend']
MemberColl = dbClient[dbName]['member']
QAColl = dbClient[dbName]['qa']
ChengyuColl = dbClient[dbName]['chengyu']
WithDrawColl = dbClient[dbName]['WithdrawMsg']
XiaokuiColl = dbClient[dbName]['personphoto']

FontPath = 'src/msyh.ttf'
FontProp = FontProperties(fname=FontPath)
BotName = '小明'
XiaoIceTimeInterval = 5 * 60
# DuilianTimeInterval = 10 * 60

QASpGroup = {}  #QA群主特权群

DuilianGroup = {}
ChengyuGroup = {}
VSGameGroup = {'机器人调教群', 'VIP休息室', '杭州知乎群', 'zmq'}
# XiaoIceGroup = [] #小冰暂时只支持一个群
# GroupNameMap = {'wzl': '温赵轮.R.熊猫减鸭会所',
#                 'zh': '知乎最牛逼兄弟会没有之一'}

NotWelcomeGroup = {'微软讨论组', '2017搜狐媒体待入职'}
NotWithDrawGroup = {'温赵轮.R.熊猫减鸭会所', 'MSP-FY17-在编人员事务群'}
NotTulingGroup = {'温赵轮.R.熊猫减鸭会所', '微软讨论组', '2017搜狐媒体待入职', 'MSP-FY17-在编人员事务群', 'Microsoft Hololens北京站'}
NotEchoGroup = {'VIP休息室', '二进制Club月亮分享秘密基地'}
NotRedPacketGroup = {'温赵轮.R.熊猫减鸭会所', '微软讨论组', '杭州知乎群'}

# NotResGroupFile = 'src/notresgroup.npy'
# if os.path.exists(NotResGroupFile):
#     NotResGroup = np.load(NotResGroupFile).tolist()
# else:
#     NotResGroup = {'二进制Club月亮分享秘密基地', '知乎最牛逼兄弟会没有之一', '产品技术部-2017校招群', 'MSMS.tech ⚔️', '微软小娜ios粉丝群', 'Build Tour 2017 GoGoGo', 'Microsoft Hololens北京站', '桑梓曳话节目群 [禁广告]', '桑梓电台微信群'}
#     np.save(NotResGroupFile, NotResGroup)
ResGroup = {'zmq', 'VIP休息室', '机器人调教群', '441饭团', '微软改名部', "Pro.Wei's fans Club", 'EE2010不散场~', '520甄宝团工作组', '吃货甄的吃货迷们☺️☺️☺️'}

class SettingEnum(Enum):
    MainOnOff = 0
    QA = 1  #QA总开关
    XiaoIceGroup = 2
    Dameng = 3
    Text2Speech = 4
Settings = {
    SettingEnum.MainOnOff: True,
    SettingEnum.QA: True,
    SettingEnum.XiaoIceGroup: '',
    SettingEnum.Dameng: False,
    SettingEnum.Text2Speech: True
     }

def generateTmpFileName(imgDir):
    return '{0}/{1}-{2}.png'.format(imgDir, int(time() * 1000), random.randint(0, 10000))

def getChatroomIdByName(names):
    chatrooms = itchat.get_chatrooms()
    groups = []
    for name in names:
        group = [x for x in chatrooms if x['NickName'] == name]
        if len(group) != 0:
            groups.append(group[0]['UserName'])
    if len(groups) == 0:
        # logging.error('Cannot find the chatrooms')
        return None
    return groups

def get_group_info(msg):
    group_id = msg['FromUserName'] if msg['FromUserName'].startswith('@@') else msg['ToUserName']
    group_name = msg['User']['NickName'] if 'User' in msg and 'UserName' in msg['User'] else 'N/A'
    if group_name not in ResGroup:
        group_id = 'filehelper'
    return group_id, group_name

def get_group_id(msg):
    return msg['FromUserName'] if msg['FromUserName'].startswith('@@') else msg['ToUserName']

def getGroupOwner(msg):
    if 'ChatRoomOwner' in msg['User']:
        return msg['User']['ChatRoomOwner']
    else:
        return msg['User']['MemberList'][0]['UserName']

def isBotOwner(msg):
    return msg['User']['Self']['UserName'] == msg['ActualUserName']

def isGroupOwner(msg):
    return getGroupOwner(msg) == msg['ActualUserName']