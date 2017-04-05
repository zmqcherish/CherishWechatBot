# -*- coding: utf-8 -*-
"""
Some utility functions
"""
import logging
import random
from time import time
import itchat

# Some global configuration
dbName = 'WechatHistory'
collName = 'history'
fontPath = 'msyh.ttf'


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
        logging.error('Cannot find the chatrooms')
        return None
    return groups
