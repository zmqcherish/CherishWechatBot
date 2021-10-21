from ProcessInterface import ProcessInterface
from itchat.content import *
from utilities import *
import itchat

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as pp

class MemberDistribution(ProcessInterface):
    def __init__(self):
        self.imgDir = 'Temp'

    def process(self, msg, type):
        if type != TEXT:
            return
        content = msg['Content']
        if not content.startswith('/v'):
           return

        group_id = get_group_id(msg)
        room = itchat.update_chatroom(group_id, detailedMember=True)

        # ower = room['MemberList'][0]['UserName']
        # if msg['ActualUserName'] != ower:
        #     return


        genderSize = [0,0,0] #[male, female, unknow]
        ulist = []
        province = {}
        for p in room['MemberList']:
            if p['Sex'] == 1:
                genderSize[0] = genderSize[0] + 1
            elif p['Sex'] == 2:
                genderSize[1] = genderSize[1] + 1
            else:
                ulist.append(p['NickName'])
                genderSize[2] = genderSize[2] + 1

            pro = p['Province']
            if pro == '':
                pro = '未知/国外'

            if pro in province:
                province[pro][0] = province[pro][0] + 1
                province[pro][1].append(p['NickName'])
            else:
                province[pro] = [1, [p['NickName']]]

        proMsg = ''
        if content != '/v':
            try:
                pro = content.split()[1]
                if pro in province:
                    proList = ','.join(province[pro][1])
                    proMsg = '{0}地区共{1}人：“{2}”'.format(pro, province[pro][0], proList)
            except Exception as e:
                logging.error(e)

        pp.figure(figsize=(7, 14))

        p1 = pp.subplot(2, 1, 1)

        labels = [u'男', u'女', u'未知']
        colors = ['lightskyblue', 'pink', 'gray']
        if genderSize[2] == 0:
            labels.pop()
            genderSize.pop()

        res = p1.pie(genderSize, labels=labels, colors=colors, labeldistance=1.1, autopct='%3.1f%%', startangle=90)
        for font in res[1]:
            font.set_fontproperties(FontProp)

        p1.axis('equal')
        # p1.set_title('群成员男女比例')
        # fn1 = generateTmpFileName(self.imgDir)
        # pp.savefig(fn1)
        # pp.clf()
        p2 = pp.subplot(2, 1, 2)
        province = sorted(province.items(), key=lambda d: d[1][0], reverse=True)

        num = 10 if len(province) > 10 else len(province)
        label2 = []
        vals2 = []
        for i in range(num):
            label2.append(province[i][0])
            vals2.append(province[i][1][0])

        if len(province) > 10:
            sum = 0
            for p in province[10:]:
                sum = sum + p[1][0]
            label2.append('其他')
            vals2.append(sum)

        res2 = p2.pie(vals2, labels=label2, labeldistance=1.1, autopct='%3.1f%%', pctdistance=0.8, startangle=90)
        for font in res2[1]:
            font.set_fontproperties(FontProp)
        p2.axis('equal')

        # pp.figure(figsize=(8, 0.4*len(province)))
        # y_pos = np.arange(len(province))
        # vals = list(province.values())
        # ylabel = list(province.keys())
        # pp.barh(y_pos, vals, align='center', height=0.4)
        # pp.yticks(y_pos, ylabel, fontproperties=self.prop)
        # pp.xlabel('人数', fontproperties=self.prop)
        # pp.title('群成员省份分布')

        fn = generateTmpFileName(self.imgDir)
        pp.savefig(fn)

        itchat.send_image(fn, group_id)
        if proMsg != '':
            itchat.send(proMsg, group_id)

        #发送未设置性别的帐号
        return
        if len(ulist) == 1:
            itchat.send(u'所以“{0}”，你的性别是?'.format(ulist[0]), group_id)
        elif len(ulist) > 1:
            ulist = ','.join(ulist)
            itchat.send(u'所以“{0}”，你们的性别是?'.format(ulist), group_id)
