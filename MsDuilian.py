from ProcessInterface import ProcessInterface
import json
import requests
from itchat.content import *
from util import *
import itchat


class MsDuilian(ProcessInterface):
    def __init__(self):
        self.header = {"Content-Type": "application/json;charset=UTF-8", "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36"}

    def process(self, msg, type):
        if type != TEXT:
            return

        content = msg['Content']
        group_id, group_name = get_group_info(msg)

        if group_name not in DuilianGroup:
            return
        if len(content) != DuilianGroup[group_name]:
            return
        input_string = {"inputString": content}
        r = requests.post('http://duilian.msra.cn/app/CoupletsWS_V2.asmx/IsValidChineseString', data=json.dumps(input_string), headers=self.header)
        if r.status_code != 200:
            return
        locker = '000000000'
        input_string ={"shanglian": content, "xialianLocker": locker[0:len(content)], "isUpdate": "false"}
        r = requests.post('http://duilian.msra.cn/app/CoupletsWS_V2.asmx/GetXiaLian', data=json.dumps(input_string), headers=self.header)
        if r.status_code != 200:
            return
        res = json.loads(r.text)
        if len(res) == 0:
            return
        res = res['d']
        xialian = random.choice(res['XialianSystemGeneratedSets'])
        xialian = random.choice(xialian['XialianCandidates'])
        itchat.send(xialian, group_id)


