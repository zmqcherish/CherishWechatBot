from itchat.content import *
from utilities import *
from ProcessInterface import ProcessInterface
import itchat
from os import path
import hashlib
import random

class VSGame(ProcessInterface):
    def __init__(self):
        self.imgDir = 'ChatImg'
        logging.info('VSGame initialized.')

    def process(self, msg, type):
        if type != PICTURE:
            return
        if isBotOwner(msg):
            return

        group_id, group_name = get_group_info(msg)

        if group_name not in VSGameGroup:
            return
        
        # md5_list = ['da1c289d4e363f3ce1ff36538903b92f', '9e3f303561566dc9342a3ea41e6552a6', 'dbcc51db2765c1d0106290bae6326fc4', '9a21c57defc4974ab5b7c842e3232671', '3a8e16d650f7e66ba5516b2780512830', '5ba8e9694b853df10b9f2a77b312cc09']
        jdstbu_list = ['f790e342a02e0f99d34b316547f9aeab', '514914788fc461e7205bf0b6ba496c49', '091577322c40c05aa3dd701da29d6423']
        fn = msg['FileName']
        gif_file = path.join(self.imgDir, fn)    
        gif_file = open(gif_file, 'rb')
        file_md5 = hashlib.md5(gif_file.read()).hexdigest()
        gif_file.close()
            
       # for i in range(6):
            #if file_md5 == md5_list[i]:
                # res = random.randint(i + 1, 6)
                #itchat.send(str(i + 1), group_id)
                # itchat.send_image('src/{}.gif'.format(res), group_id)
              #  break
        
        for i in range(3):
            if file_md5 == jdstbu_list[i]:
                if i == 0:
                    itchat.send_image('src/game/bu.gif', group_id)
                elif i == 1:
                    itchat.send_image('src/game/st.gif', group_id)
                else:
                    itchat.send_image('src/game/jd.gif', group_id)
                break
