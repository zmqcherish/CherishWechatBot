from ProcessInterface import ProcessInterface
import os
from itchat.content import *
from utilities import *

class MicoIce(ProcessInterface):
    def __init__(self):
        self.imgDir = 'ChatImg'
        self.mpNum = itchat.search_mps(name='小冰')

    def process(self, msg, type):
        if Settings[SettingEnum.XiaoIceGroup] == '':
            return

        if msg['User']['NickName'] == '小冰' or msg['User']['Alias'] == 'xiaoice-ms':  #小冰
            if type == TEXT:
                itchat.send(msg['Text'], Settings[SettingEnum.XiaoIceGroup])
            elif type == PICTURE:
                fn = msg['FileName']
                new_fn = os.path.join(self.imgDir, fn)
                msg['Text'](fn)
                os.rename(fn, new_fn)
                itchat.send_image(new_fn, Settings[SettingEnum.XiaoIceGroup])
            elif type == VOICE:
                itchat.send('[无法发送的消息]', Settings[SettingEnum.XiaoIceGroup])
        else:   #群聊
            group_id = get_group_id(msg)
            if group_id != Settings[SettingEnum.XiaoIceGroup] or isBotOwner(msg):
                return
            if type == TEXT:
                content = msg['Content']
                if content in ['变身', '停止变身']: #, '/v', '/bing', '/bing -r', '/tag', '/tagcloud', '/activity', '/mytag', '/last', '/help']:
                    return
                if content.startswith('/'): #不响应
                    return
                itchat.send(content, self.mpNum[0]['UserName'])
            elif type == PICTURE:
                fn = msg['FileName']
                new_fn = os.path.join(self.imgDir, fn)
                # msg['Text'](fn)
                # os.rename(fn, new_fn)
                itchat.send_image(new_fn, self.mpNum[0]['UserName'])


