from ProcessInterface import ProcessInterface
import itchat
from random import randint
from utilities import get_group_info

class EasterEgg(ProcessInterface):
    group = []
    emoji = 'src/emoji/1.gif'
    def __init__(self):
        print('EasterEgg initialized.')

    def process(self, msg, type):
        group_id, group_name = get_group_info(msg)

        if group_name not in self.group:
            return
        
        i = randint(0, 49)
        # itchat.send(str(i), group_id)
        if i == 0:
            itchat.send_image(self.emoji, group_id)
