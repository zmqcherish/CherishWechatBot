from itchat.content import *
from utilities import *
from ProcessInterface import ProcessInterface
import itchat
import requests

class Tuling(ProcessInterface):
    def __init__(self):
        logging.info('Tuling initialized.')

    def process(self, msg, type):
        if type != TEXT:
            return
        if not msg['IsAt']:
            return
        group_id, group_name = get_group_info(msg)

        if group_name in NotTulingGroup:
            return

        content = msg['Content'].split()[-1]
        data = {'key': '7bd331e1cc214596865abce7689dc32c', 'info': content, 'userid': 'cherish-bot'}
        r = requests.post('http://www.tuling123.com/openapi/api', data=data).json()
        itchat.send(r['text'], group_id)
