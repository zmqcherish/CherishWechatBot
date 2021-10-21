import itchat
# from itchat.content import *
from apscheduler.schedulers.blocking import BlockingScheduler
from lean_cloud import *
from time import sleep
from datetime import datetime

itchat.auto_login(True, enableCmdQR=2)
# itchat.auto_login(True)
scheduler = BlockingScheduler()

main_gid = ''
persons = [{'name':'安安','val':['753358591']},{'name':'兔子','val':[]},{'name':'大仙','val':[]},{'name':'雕工','val':['-991086710']},{'name':'队长','val':[]},{'name':'朵拉','val':[]},{'name':'雪总','val':['-1070059135']},{'name':'HJK ','val':['672870504']},{'name':'后来','val':['-564810513']},{'name':'荒荒','val':[]},{'name':'渺小','val':['-822447189']},{'name':'七秒','val':[]},{'name':'阿姨','val':[]},{'name':'刀刀','val':[]},{'name':'田瓜','val':[]},{'name':'谈谈','val':['-224678619']},{'name':'小蓝','val':['-1427137943']},{'name':'小孩','val':['-26769386']},{'name':'雯雯','val':['-961697283']},{'name':'无题','val':['1995828037']},{'name':'咸鱼','val':['988382084']},{'name':'微微','val':['316324625']},{'name':'徐佳','val':['1746137973']},{'name':'大海','val':['-161872783']},{'name':'一只鹿','val':['18467']},{'name':'田田圈330','val':[]}]
# @itchat.msg_register([TEXT], isGroupChat=True)
# def text_reply(msg):
# 	global has_update
# 	if not has_update:
# 		return
# 	group_id = msg['FromUserName'] if msg['FromUserName'].startswith('@@') else msg['ToUserName']
# 	group_name = msg['User']['NickName'] if 'User' in msg and 'UserName' in msg['User'] else 'N/A'
# 	if group_name == 'mes':
# 		a=1
# 		itchat.send('sss', group_id)
# 		print(group_id)
# 	has_update = False

def getChatroomIdByName(name):
	chatrooms = itchat.get_chatrooms(True)
	group = [x for x in chatrooms if x['NickName'] == name]
	if len(group) > 0:
		return group[0]['UserName']


def send_msg():
	msg = []
	for p in persons:
		count = 0
		for v in p['val']:
			a = find_by_cid(v)
			if a:
				count += a.get('count')
		if count == 0:
			msg.append(f"{p['name']}:")
		else:
			msg.append(f"{p['name']}:{count}")
	msg.append('xmgg:0')
	msg.append(datetime.now().strftime('%m/%d') + ' 号')
	itchat.send('\n'.join(msg), main_gid)
	a=1


def main():
	a = find_by_cid('19830330')
	has_update = a.get('update')
	if not has_update:
		return
	logging.info('has update')
	send_msg()
	update_update(False)


def init2():
	for p in persons:
		for v in p['val']:
			a = find_by_cid(v)
			if not a:
				save_val(v, 0, p['name'])
	update_update(False)


def init():
	for p in persons:
		for v in p['val']:
			a = find_by_cid(v)
			if a:
				update_val(v, 0)
	update_update(False)


def getm():
	print(1111)
	uu = []
	gid = getChatroomIdByName('小樂手hebetien.club')
	room = itchat.update_chatroom(gid, detailedMember=True)
	aa = room['MemberList']
	for p in aa:
		print(p['NickName'])
		uu.append(p['NickName'])
	print(uu)

# init2()
if __name__ == '__main__':
	itchat.run(blockThread=False)
	getm()
	#scheduler.add_job(main, 'cron', second='0', minute='0/1', hour='*', day='*', month='*')
	#scheduler.add_job(init, 'cron', second='0', minute='0', hour='0', day='1/1', month='*')
	#scheduler.start()
