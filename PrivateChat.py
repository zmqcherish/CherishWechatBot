from itchat.content import *
from utilities import *
from ProcessInterface import ProcessInterface
import itchat
import requests

class PrivateChat(ProcessInterface):
    def __init__(self):
        self.shuyang_person = {}
        logging.info('PrivateChat initialized.')
        pass

    def process(self, msg, type):
        if type != TEXT:
            return

        content = msg['Content']
        personId = msg['FromUserName']

        if content.startswith('-'): #图灵机器人对话
            content = content[1:]
            apiUrl = 'http://www.tuling123.com/openapi/api'
            data = {'key': '7bd331e1cc214596865abce7689dc32c', 'info': content, 'userid': 'cherish-bot'}
            r = requests.post(apiUrl, data=data).json()
            itchat.send(r['text'], personId)
            return
        
        if content.startswith('/'):
            return
        if content == '数羊':
            if personId in self.shuyang_person:
                return
            self.shuyang_person[personId] = 1
            itchat.send('乖，睡不着了吗？我来陪你数羊吧，伴你香甜如梦，我先来，[1只羊]咩咩叫，该你了。。。说"不数了"就可以停止数羊～', personId)
            return

        if personId not in self.shuyang_person: #包括自己说话不处理
            return
        if content == '不数了':
            del self.shuyang_person[personId]
            itchat.send('怎么不数了，是困了吗，早点睡觉哦～晚安',personId)
            return
        if not re.match('[1-9][0-9]?[0-9]?只羊', content):
            itchat.send('该你数羊了，我数到{0}只羊了'.format(self.shuyang_person[personId]), personId)
            return

        # 数羊
        count = int(content[:-2])
        record = self.shuyang_person[personId]
        if count == record + 1:
            self.shuyang_person[personId] = count + 1
            res = '{0}只羊'.format(count + 1)
            if count == 100:
                res = '你怎么这么能数，我都快数不动了...' + res
            itchat.send(res, personId)
        else:
            itchat.send('不对啦，你应该是{0}只羊'.format(record + 1), personId)
            
