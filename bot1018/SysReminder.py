from ProcessInterface import ProcessInterface
from itchat.content import *
from utilities import *
import itchat
from threading import Thread
from time import sleep
from xml.etree import ElementTree

def withdrawBlockEnd(groupId, blockTime):
    sleep(blockTime)
    if groupId in NotWithDrawGroup:
        NotWithDrawGroup.remove(groupId)
        itchat.send('防撤回功能已打开', groupId)

class SysReminder(ProcessInterface):
    def __init__(self):
        self.withdrawCount = 0
        self.withdrawTotal = 10
        self.withdrawTimeInterval = 60
        self.withdrawFirstTime = 0
        self.withdrawBlockTime = 5 * 60

    def process(self, msg, type):
        if type != NOTE:
            return

        content = msg['Content']
        group_id, group_name = get_group_info(msg)

        if 'invited' in content or u'邀请' in content or u'通过扫描' in content or 'QR' in content:
            # roomId = getChatroomIdByName([groupName])
            # if roomId is None:
            #     return
            if group_name in NotWelcomeGroup:
                return

            room = itchat.update_chatroom(group_id, detailedMember=True)
            p = room['MemberList'][-1]
            # if p['Sex'] == 1:
            #     res = '👏帅哥“{}”加入,我的技能列表：'.format(p['NickName'])
            # elif p['Sex'] == 2:
            #     res = '👏美女“{}”加入,我的技能列表：'.format(p['NickName'])
            # else:
            #     res = '👏“{}”加入。我的技能列表：'.format(p['NickName'])
            res = '👏“{}”加入。指令"/help"可查看bot技能列表'.format(p['NickName'])
            itchat.send(res, group_id)
            # itchat.send_image('src/help.png', group_id)
            return

        if msg['MsgType'] == 10002:
            if group_name in NotWithDrawGroup:
                group_id = 'filehelper'
                # return

            # if msg['User']['IsOwner']:
            #     return
            if msg['Text'] == '你撤回了一条消息':  #自己发的不做处理
                return

            #if msg['ActualUserName'] == getGroupOwner(msg):    #群主发的不处理
             #   itchat.send(u'群主特权！不让你们看撤回～', groupId)
              #  groupId = 'filehelper'
                # return

            #防止恶意撤回
            if self.withdrawCount == 0:
                self.withdrawFirstTime = int(time())
            if self.withdrawCount == self.withdrawTotal:
                self.withdrawCount = 0
                if int(time()) - self.withdrawFirstTime < self.withdrawTimeInterval:
                    NotWithDrawGroup.append(group_id)
                    itchat.send('检测到恶意撤回，防撤回功能自动关闭{0}分钟'.format(int(self.withdrawBlockTime / 60)), group_id)
                    Thread(target=withdrawBlockEnd, args=[group_id, self.withdrawBlockTime]).start()
                    return

            self.withdrawCount = self.withdrawCount + 1

            name = msg['ActualNickName']
            xml = ElementTree.fromstring(content)
            msg_id = xml.find('revokemsg').find('msgid').text
            record = list(HisColl.find({'msgId': msg_id}))
            if len(record) == 0:
                return
            
            text = record[0]['content']
            msg_type = record[0]['type']
            if msg_type == PICTURE:
                itchat.send('“{}”撤回了一张见不得人的图片：\n'.format(name), group_id)
                itchat.send_image(text, group_id)
            elif msg_type == VOICE:
                itchat.send('“{}”撤回了一条见不得人的语音：\n'.format(name), group_id)
                itchat.send_file(text, group_id)
            else:
                itchat.send('“{}”撤回了一条见不得人的消息：\n{}'.format(name, text), group_id)

            logging.info('“{}”撤回了一条消息：\n{}'.format(name, text))
            WithDrawColl.insert({'msgId': msg_id, 'msgtype': msg_type, 'name': name, 'content': text, 'group': group_name, 'timestamp': record[0]['timestamp'], 'time': record[0]['time']})
            return

        if msg['MsgType'] == 1e4 and ('红包' in content or 'Red' in content):
            if group_name not in NotRedPacketGroup:
                itchat.send('[系统消息]有人发红包！', group_id)
            text = '[{0}]有人发红包'.format(group_name)
            itchat.send(text, 'filehelper')
            logging.info(text)
            # return
        
        # if msg['MsgType'] == 1e4 and '修改群名' in content:
        #     if group_name in NotResGroup:
        #         NotResGroup.remove(group_name)
        #         left = content.find('“') + 1
        #         right= content.find('”')
        #         NotResGroup.add(content[left: right])
        #         np.save(NotResGroupFile, NotResGroup)