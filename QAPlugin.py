from itchat.content import *
from utilities import *
from ProcessInterface import ProcessInterface
from datetime import datetime
import itchat

class QAPlugin(ProcessInterface):
    def __init__(self):
        # self.collName = 'QA'
        # self.coll = DbClient[dbName][self.collName]
        logging.info('QAPlugin initialized.')
        #self.content_map = {'小葵': 'src/person/xk.gif', '登登': 'src/person/dd.gif', '兔子': 'src/person/tz.png', '小明': 'src/person/xm.png', '梦': 'src/person/meng.gif', '小灵儿': 'src/person/xle.gif'}

    def process(self, msg, type):
        if not Settings[SettingEnum.QA]:
            return

        if type != TEXT:
            return

        content = msg['Content']
        group_id, group_name = get_group_info(msg)

        if content.startswith('/t '):
            qa = content.split()
            if len(qa) == 3:
                question = qa[1]
                answer = qa[2]
                if question == '变身':
                    return
                if answer.startswith('@'):
                    itchat.send(u'还想坑我[机智]', group_id)
                    return

                SpChatRoomIds = getChatroomIdByName(QASpGroup)
                if (SpChatRoomIds is not None) and (group_id in SpChatRoomIds):
                    if msg['ActualUserName'] != getGroupOwner(msg):
                        itchat.send('怕你们玩坏我，现在暂时只听群主的话！', group_id)
                        return


                query = {'question': question, 'to': group_name}

                timestamp = time()
                rtime = datetime.fromtimestamp(timestamp)
                record = {
                    'question': question,
                    'answer': answer,
                    'from': msg['ActualNickName'],
                    'fromId': msg['ToUserName'],
                    'to': group_name if 'User' in msg and 'UserName' in msg['User'] else 'N/A',
                    'timestamp': timestamp,
                    'time': rtime
                }
                res = list(QAColl.find(query))
                if len(res) == 1:
                    if isBotOwner(msg):
                        if answer == '-':
                            QAColl.remove(query)
                        else:
                            QAColl.update(query, record)
                    else:
                        itchat.send('我知道答案，不用你教我~', group_id)
                else:
                    QAColl.insert(record)
                    itchat.send(u'so easy! 我记住了，不信你考我！', group_id)
                    logging.info('QA remember:{0}:{1}'.format(question, answer))
        elif content == '/t':
            res = list(QAColl.find({'to': group_name}))
            if len(res) == 0:
                return
            qa_s = ['{}：{}'.format(r['question'], r['answer']) for r in res]
            qa_s = '\n'.join(qa_s)
            itchat.send('调教列表：\n' + qa_s, group_id)
        else:
            if isBotOwner(msg):
                return
            #if content in self.content_map and group_name == 'VIP休息室':
             #   itchat.send_image(self.content_map[content], group_id)
            res = list(QAColl.find({'question': content, 'to': group_name}))
            if len(res) == 1:
                itchat.send(res[0]['answer'], group_id)
