import http.client
from xml.etree import ElementTree
from ProcessInterface import ProcessInterface
from utilities import *
import itchat
from threading import Thread
from time import sleep

def blockEnd():
    sleep(60)
    Settings[SettingEnum.Text2Speech] = True

# Note: The way to get api key:
# Free: https://www.microsoft.com/cognitive-services/en-us/subscriptions?productId=/products/Bing.Speech.Preview
# Paid: https://portal.azure.com/#create/Microsoft.CognitiveServices/apitype/Bing.Speech/pricingtier/S0

class BingText2Speech(ProcessInterface):
    def __init__(self):
        self.apiKey = "dc94e5bed53e459695e127095d33cc0c"
        self.count = 0
        self.startTime = 0

    def process(self, msg, type):
        if not Settings[SettingEnum.Text2Speech]:
            return
        text = msg['Content']
        if not text.startswith('/s '):
            return
        group_id, group_name = get_group_info(msg)
        # 防止使用过度
        if self.count == 0:
            self.startTime = int(time())
        if self.count == 10:
            self.count = 0
            if int(time()) - self.startTime < 60:
                Settings[SettingEnum.Text2Speech] = False
                itchat.send('使用过度，暂停使用', group_id)
                Thread(target=blockEnd).start()
                return

        if not isBotOwner(msg):
            self.count = self.count + 1

        params = ""
        headers = {"Ocp-Apim-Subscription-Key": self.apiKey}

        # AccessTokenUri = "https://api.cognitive.microsoft.com/sts/v1.0/issueToken";
        AccessTokenHost = "api.cognitive.microsoft.com"
        path = "/sts/v1.0/issueToken"

        # Connect to server to get the Access Token
        # print("Connect to server to get the Access Token")
        conn = http.client.HTTPSConnection(AccessTokenHost)
        conn.request("POST", path, params, headers)
        response = conn.getresponse()
        # print(response.status, response.reason)
        data = response.read()
        conn.close()
        if response.status != 200:
            return

        accesstoken = data.decode("UTF-8")

        body = ElementTree.Element('speak', version='1.0')
        body.set('{http://www.w3.org/XML/1998/namespace}lang', 'zh-CN')
        voice = ElementTree.SubElement(body, 'voice')
        voice.set('{http://www.w3.org/XML/1998/namespace}lang', 'zh-CN')
        voice.set('{http://www.w3.org/XML/1998/namespace}gender', 'Female')
        voice.set('name', 'Microsoft Server Speech Text to Speech Voice (zh-CN, HuihuiRUS)')
        voice.text = text[3:]

        reqHeaders = self.getHeader(accesstoken)

        conn = http.client.HTTPSConnection("speech.platform.bing.com")
        conn.request("POST", "/synthesize", ElementTree.tostring(body), reqHeaders)
        response = conn.getresponse()
        # print(response.status, response.reason)

        data = response.read()
        conn.close()
        if response.status == 200:
            with open('Temp/msg.mp3', 'wb') as f:
                f.write(data)
            itchat.send_file('Temp/msg.mp3', group_id)
        # print("The synthesized wave length: %d" % (len(data)))

    def getHeader(self, accesstoken):
        return {"Content-type": "application/ssml+xml",
                "X-Microsoft-OutputFormat": "audio-16khz-64kbitrate-mono-mp3",
                "Authorization": "Bearer " + accesstoken,
                "X-Search-AppId": "07D3234E49CE426DAA29772419F436CA",
                "X-Search-ClientID": "1ECFAE91408841A480F00935DC390960",
                "User-Agent": "TTSForPython"}
