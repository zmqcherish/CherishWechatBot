from utilities import *
from ProcessInterface import ProcessInterface
import requests
import os
import itchat
from itchat.content import *
from datetime import datetime
from urllib.request import urlretrieve
from urllib.request import urlopen
import json
from pymongo import DESCENDING
from bs4 import BeautifulSoup

class KeyHandler(ProcessInterface):
    def __init__(self):
        self.help_imgpath = 'src/help.png'
        self.imgDir = 'Temp'
        self.group_id = ''
        self.hebeUrl = open('src/hebe.txt').readlines()
        self.damengId = '@105d3294baedcb135b0b0cb544551097'  # 大萌
        self.hebe = ['hebe', 'Hebe', '田馥甄', 'HEBE', '馥甄']
        self.h = ['³³⁰', '⁵²⁰', '₃₃₀', '₅₂₀', 'ᴴᵉᵇᵉ', 'ᴴᵉᵇᵉ', 'ᴴᵉᵇᵉ', 'ꓱꓭꓱꓧ', 'ꓱꓭꓱꓧ', '♥', 'hebe', 'hebe']
        self.six = ['₆₆₆₆₆₆', '⁶⁶⁶⁶⁶⁶', '666666']
        self.twothree = ['²³³³³³³', '₂₃₃₃₃₃₃', '2333333']
        self.cmd = '/on  打开 /off 关闭\n\n全局，所有群\n/on			打开机器人\n/on -m		打开大萌说的话\n/on -t2s	文本转语音\n\n针对特定群\n/on -all		打开机器人功能\n/on -sz		打开筛子游戏\n/on -t -y	打开调教功能，群主专属\n/on -t -n	打开调教功能，非群主专属\n/off -t		关闭调教功能\n/on -wd		防撤回功能\n/on -tl		图灵对话\n/on -w		欢迎新人'
        logging.info('KeyHandler initialize.')

    def process(self, msg, type):
        # if not OnOffs[PluginName.Key]:
        #     return
        if type != TEXT:
            return

        content = msg['Content']
        self.group_id, group_name = get_group_info(msg)
        if content[-1] == '#':  #自动撤回
            self.revokeMsg(msg['MsgId'])

        elif content == '/m': #大萌语句
            if not Settings[SettingEnum.Dameng]:
                return
            logging.info(group_name + ': m')
            # i = random.randint(0, 1)
            i = 0
            if i == 0:
                records = list(HisColl.find({'to': group_name, 'userName': self.damengId}))
                if len(records) == 0:
                    return
                record = random.choice(records)
                text = '大萌曾经说过：' + record['content']
                itchat.send(text, self.group_id)
            else:  # 1
                # 发图
                pass

        elif content == '/help':    #帮助文档
            logging.info(group_name + ': help')
            itchat.send_image(self.help_imgpath, self.group_id)

        elif content == '/bing' or content == '/bing -r':   #必应壁纸
            logging.info(group_name + ': bing')
            if msg['Content'] == '/bing':  # 取当天的壁纸
                fn = 'src/bing/{0}.jpg'.format(datetime.now().strftime('%Y-%m-%d'))
                if not os.path.isfile(fn):
                    url = 'http://www.bing.com/HPImageArchive.aspx?format=js&idx=0&n=1'
                    with urlopen(url) as f:
                        data = f.read()
                    img = data.decode('utf-8')
                    img = json.loads(img)
                    imgUrl = 'http://www.bing.com' + img['images'][0]['url']
                    urlretrieve(imgUrl, fn)
            else:
                fn = 'src/bing/' + random.choice(os.listdir('Bing'))
            itchat.send_image(fn, self.group_id)
        elif content.startswith('/wd'):
            index = 1
            if content != '/wd':
                index = int(content[-1])
            record = list(WithDrawColl.find({'group': group_name}).sort([('timestamp', DESCENDING)]).limit(index))[-1]
            
            name = record['name']
            text = record['content']
            msg_type = record['msgtype']
            if msg_type == PICTURE:
                itchat.send('“{}”撤回了一张见不得人的图片：\n'.format(name), self.group_id)
                itchat.send_image(text, self.group_id)
            elif msg_type == VOICE:
                itchat.send('“{}”撤回了一条见不得人的语音：\n'.format(name), self.group_id)
                itchat.send_file(text, self.group_id)
            else:
                itchat.send('“{}”撤回了一条见不得人的消息：\n{}'.format(name, text), self.group_id)
        # elif content == '/cat':
        #     logging.info(group_name + ': cat')
        #     r = requests.get('http://random.cat/meow').json()
        #     self.send_img(r['file'])
        # elif content == '/food':
        #     logging.info(group_name + ': food')
        #     imgUrl = 'http://lorempixel.com/400/200/food/'
        #     self.send_img(imgUrl)
        # elif content == '/dog':
        #     logging.info(group_name + ': dog')
        #     url = 'http://random.dog/'
        #     html = urlopen(url)
        #     soup = BeautifulSoup(html.read(), 'html.parser')
        #     img = soup.find('img')
        #     imgUrl = url + str(img['src'])
        #     self.send_img(imgUrl)

        elif content in self.hebe:
            logging.info(group_name + ': hebe')
            imgUrl = random.choice(self.hebeUrl)
            self.send_img(imgUrl)
        elif content == '/h':
            logging.info(group_name + ': h')
            res = ''
            for i in range(100):
                res += random.choice(self.h) + '    '
            itchat.send(res, self.group_id)
        elif content == '/2':
            logging.info(group_name + ': 233')
            res = ''
            for i in range(50):
                res += random.choice(self.twothree) + '    '
            itchat.send(res, self.group_id)
        elif content == '/6':
            logging.info(group_name + ': 666')
            res = ''
            for i in range(50):
                res += random.choice(self.six) + '    '
            itchat.send(res, self.group_id)
        elif content == '/about':
            logging.info(group_name + ': about')
            itchat.send('bot使用python开发。由于网络和服务器的问题，bot有时候不稳定，十分抱歉。如果有特别有意思的使用场景意见，欢迎私聊留言。', self.group_id)
        elif content == '/cmd': #隐藏功能
            itchat.send(self.cmd, self.group_id)

        elif content == '/update':
            # if not isBotOwner(msg):
            #     return
            return
            logging.info(group_name + ': update')
            room = itchat.update_chatroom(self.group_id, detailedMember=True)
            members = room['MemberList']
            # memberIds = []
            memberNames = []
            for m in members:
                # memberIds.append(m['UserName'])
                memberNames.append(m['NickName'])
            # idStr = ' '.join(memberIds)
            nameStr = '|||'.join(memberNames)
            r = list(self.collGroup.find({'group': group_name}))
            if len(r) > 0:
                leavelPerson = []
                r = r[0]
                # oldIdStr = r['idStr']
                # oldIds = oldIdStr.split()
                oldNameStr = r['nameStr']
                oldNames = oldNameStr.split('|||')
                for i in range(len(oldNames)):
                    if oldNames[i] not in memberNames:
                        leavelPerson.append(oldNames[i])
                if len(leavelPerson) > 0:
                    leavelPerson = ','.join(leavelPerson)
                    itchat.send('“{0}”退群了'.format(leavelPerson), self.group_id)

            insertData = {'group': group_name, 'nameStr': nameStr}
            MemberColl.update({'group': group_name}, insertData, upsert=True)
            # itchat.send('"{}"群成员已更新'.format(groupName), self.groupId)
            itchat.send('群名单已更新', self.group_id)

    def send_img(self, imgUrl):
        fn = generateTmpFileName(self.imgDir)
        urlretrieve(imgUrl, fn)
        itchat.send_image(fn, self.group_id)

    def revokeMsg(self, msgId):
        url = 'https://wx.qq.com/cgi-bin/mmwebwx-bin/webwxrevokemsg'
        data = {
            'BaseRequest': itchat.instanceList[0].loginInfo['BaseRequest'],
            'SvrMsgId': msgId,
            'ToUserName': self.group_id,
            'ClientMsgId': int(time() * 1e4)
        }
        headers = {'ContentType': 'application/json; charset=UTF-8',
                   'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36'}
        r = requests.post(url, headers=headers, data=json.dumps(data), cookies=itchat.instanceList[0].s.cookies)
        a = 1

    # def sendVoice(self, msg):
    #     self.groupId = getGroupId(msg)
    #     groupName = msg['User']['NickName']
    #     # itchat.send_file('img/mask.png',self.groupId,'ZCtZqGr8mNFdMHHFw4LlFaVle46NiOCFHa3q0vJdeFTJtNqBxil0bDwKHtF3elEK')
    #     # return
    #     # msgId = msg['MsgId']
    #     url = 'https://wx.qq.com/cgi-bin/mmwebwx-bin/webwxsendmsgvoice'
    #     params = {
    #         'pass_ticket': itchat.instanceList[0].loginInfo['pass_ticket'],
    #         'fun': 'async',
    #         'f': 'json',
    #         'lang': 'zh_CN'
    #     }
    #     clientMsgId = int(time() * 1e4)
    #     data = {
    #         'BaseRequest': itchat.instanceList[0].loginInfo['BaseRequest'],
    #         'Scene': 0,
    #         'Msg': {
    #             'Type': 34,#VOICE
    #             'MediaId': 'ZCtZqGr8mNFdMHHFw4LlFaVle46NiOCFHa3q0vJdeFTJtNqBxil0bDwKHtF3elEK',
    #             'FromUserName': msg['User']['Self']['UserName'],
    #             'ToUserName': 'filehelper',
    #             'LocalId': clientMsgId,
    #             'ClientMsgId': clientMsgId
    #         }
    #     }
    #
    #     headers = {'ContentType': 'application/json; charset=UTF-8',
    #                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36'}
    #     r = requests.post(url, headers=headers,params=params, data=json.dumps(data), cookies=itchat.instanceList[0].s.cookies)
    #     a=1
