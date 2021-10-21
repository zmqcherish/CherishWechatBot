from ProcessInterface import ProcessInterface
from itchat.content import *
from util import *
import itchat
# import pypinyin as py
# import requests


class ChengYuJieLong(ProcessInterface):
    def __init__(self):
        self.cy_list = []
        pass

    def process(self, msg, type):
        if type != TEXT:
            return

        content = msg['Content']
        # if content.startswith('add '):
        #     item = content.split(' ')
        #     if len(list(ChengyuColl.find({'cy': item[1]}))) == 1:
        #         itchat.send('已存在', 'filehelper')
        #         return
        #     ChengyuColl.insert({'cy': item[1], 'first': item[2], 'second': item[3], 'third': item[4], 'last': item[-1]})
        #     itchat.send('插入成功', 'filehelper')
        #     return
        if len(content) != 4 or content == '成语接龙':
            return

        group_id, group_name = get_group_info(msg)

        if group_name not in chengyu_group:
            return

        cy = select_item_with_sql("select * from chengyu where cy='{}'".format(content))
        if len(cy) == 0:
            return
        # if len(cy) == 0:
        #     r = requests.get('http://i.itpk.cn/api.php?question=@cy{}'.format(content))
        #     answer = r.text.replace('\ufeff', '')
        #     if answer.find('4') == -1:
        #         print('网络获取........')
        #         itchat.send(answer, group_id)
        #         cypy = py.pinyin(answer, style=py.NORMAL)
        #         ChengyuGroup[group_name] = cypy[-1][0]
        #         self.cy_list.add('{} {}'.format(answer, ' '.join([i[0] for i in cypy])))
        #         np.save('src/cylist.npy', self.cy_list)
        #     return
        if cy[0]['first'] != chengyu_group[group_name]:
            # itchat.send('错误', groupId)
            return
        answers = select_item_with_sql("select * from chengyu where first='{}'".format(cy[0]['last']))
        if len(answers) == 0:
            # itchat.send('我不会', group_id)
            pass
        else:
            answer = random.choice(answers)
            chengyu_group[group_name] = answer['last']
            itchat.send(answer['cy'], group_id)
