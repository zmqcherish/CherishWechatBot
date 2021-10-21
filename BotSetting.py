from ProcessInterface import ProcessInterface
from itchat.content import *
from util import *
import itchat
import re
from threading import Thread
from time import sleep


def XiaoIceEnd():
    sleep(XiaoIceTimeInterval)
    Settings[SettingEnum.QA] = True #打开调教
    if Settings[SettingEnum.XiaoIceGroup] != '':
        itchat.send('【时间到，停止变身】', Settings[SettingEnum.XiaoIceGroup])
        Settings[SettingEnum.XiaoIceGroup] = ''

# def DuilianEnd(groupId):
#     sleep(DuilianTimeInterval)
#     if groupId in DuilianGroup:
#         del DuilianGroup[groupId]
#         itchat.send('【时间到，结束对联模式】', groupId)


class BotSetting(ProcessInterface):
    def __init__(self):
        pass

    def process(self, msg, type):
        if type != TEXT:
            return

        content = msg['Content']
        group_id, group_name = get_group_info(msg)

        ##对联设置
        # if msg['User']['Self']['UserName'] == msg['ActualUserName']:  #机器人帐号专属权利
        if re.match('对联模式[3-9]', content):
            num = int(content[-1])
            DuilianGroup[group_name] = num
            text = '{}字对联模式开启，输入{}个汉字我就会给出下联，来试试吧～'.format(num, num)
            if Settings[SettingEnum.XiaoIceGroup] == group_id:
                text = text + '(自动停止变身)'
                Settings[SettingEnum.XiaoIceGroup] = ''
            itchat.send(text, group_id)
        elif content == '对联结束':
            if group_name not in DuilianGroup:
                return
            del DuilianGroup[group_name]
            itchat.send('【对联模式结束】', group_id)

        elif content == '成语接龙':
            cy = random.choice(select_item_with_sql('select * from chengyu'))
            chengyu_group[group_name] = cy['last']
            text = '成语接龙模式开启，我先来：\n{}'.format(cy['cy'])
            if Settings[SettingEnum.XiaoIceGroup] == group_id:
                text = text + '(自动停止变身)'
                Settings[SettingEnum.XiaoIceGroup] = ''
            itchat.send(text, group_id)
        elif content == '结束成语接龙':
            if group_name not in chengyu_group:
                return
            del chengyu_group[group_name]
            itchat.send('【成语接龙模式结束】', group_id)

        elif content == '变身':
            # if not isBotOwner(msg) and not isGroupOwner(msg):
            #     itchat.send(u'你叫我变就变，你谁啊？只能群主和我自己才能让我变身', groupId)
            #     return
            if Settings[SettingEnum.XiaoIceGroup] == '':
                text = '变身模式开启！只有{0}分钟时间，你们要珍惜哦～(无法响应商城表情)'.format(int(XiaoIceTimeInterval / 60))
                if group_id in DuilianGroup:
                    text = text + '(对联模式自动关闭)'
                itchat.send(text, group_id)
                Settings[SettingEnum.XiaoIceGroup] = group_id
                Thread(target=XiaoIceEnd).start()   #开启定时器
                Settings[SettingEnum.QA] = False    #关闭调教
            elif Settings[SettingEnum.XiaoIceGroup] == group_id:
                itchat.send('已经处于变身状态呢！', group_id)
            else:
                itchat.send('变身失败，变身模式已在其他群使用，目前暂时只支持一个群。', group_id)
        elif content == '停止变身':
            # if not isBotOwner(msg):
            #     itchat.send(u'我就不！变身好玩～', groupId)
            #     return
            itchat.send('不变了，好累！', group_id)
            Settings[SettingEnum.XiaoIceGroup] = ''


        if not (content.startswith('/on') or content.startswith('/off')):
            return
        if not isBotOwner(msg):
            itchat.send('抱歉，你没有权限', group_id)
            return

        if content == '/on':
            itchat.send('机器人功能已打开，输入指令"/help"查看调教指南', group_id)
            # itchat.send_image('img/help.png', group_id)
            Settings[SettingEnum.MainOnOff] = True
        elif content == '/off':
            itchat.send('再见', group_id)
            Settings[SettingEnum.MainOnOff] = False

        if content == '/on -all':
            itchat.send('机器人功能已打开', group_id)
            if group_name not in ResGroup:
                ResGroup.add(group_name)
        elif content == '/off -all':
            if group_name in ResGroup:
                ResGroup.remove(group_name)

        elif content == '/on -t -y':    # 群主专属
            itchat.send('调教功能已打开。不过怕你们玩坏我，现在暂时只听群主的话！', group_id)
            Settings[SettingEnum.QA] = True
            QASpGroup.add(group_name)
        elif content == '/on -t -n':    # 非群主专属
            itchat.send('调教功能已打开', group_id)
            Settings[SettingEnum.QA] = True
            if group_name in QASpGroup:
                QASpGroup.remove(group_name)
        elif content == '/off -t':
            itchat.send('调教功能已关闭', group_id)
            Settings[SettingEnum.QA] = False

        elif content == '/on -wd':
            pass
            # itchat.send('防撤回功能已打开', group_id)
            # if group_name in NotWithDrawGroup:
            #     NotWithDrawGroup.remove(group_name)
        elif content == '/off -wd':
            pass
            # itchat.send('防撤回功能已关闭', group_id)
            # NotWithDrawGroup.add(group_name)

        elif content == '/on -tl':
            if group_name in NotTulingGroup:
                NotTulingGroup.remove(group_name)
        elif content == '/off -tl':
            NotTulingGroup.add(group_name)

        elif content == '/on -w':
            pass
            # if group_name in NotWelcomeGroup:
            #     NotWelcomeGroup.remove(group_name)
        elif content == '/off -w':
            pass
            # NotWelcomeGroup.add(group_name)

        elif content == '/off -sz':
            if group_name in VSGameGroup:
                VSGameGroup.remove(group_name)
        elif content == '/on -sz':
            itchat.send('开始筛子游戏', group_id)
            VSGameGroup.add(group_name)

        elif content == '/on -m':
            Settings[SettingEnum.Dameng] = True
        elif content == '/off -m':
            Settings[SettingEnum.Dameng] = False

        elif content == '/on -t2s':
            Settings[SettingEnum.Text2Speech] = True
        elif content == '/off -t2s':
            Settings[SettingEnum.Text2Speech] = False


