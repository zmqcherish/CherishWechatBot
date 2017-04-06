from pymongo import MongoClient, DESCENDING
from utilities import *
from ProcessInterface import ProcessInterface
import numpy as np
from PIL import Image
from wordcloud import WordCloud
import os
import re
import itchat
from itchat.content import *
import jieba
from collections import Counter
from urllib.request import urlretrieve
from urllib.request import urlopen
import json
from bs4 import BeautifulSoup

class GroupTagCloud(ProcessInterface):
    recordMaxNum = 500
    maxFrequency = 40
    imgDir = 'TagCloud'

    def __init__(self, maskPath = None):
        self.client = MongoClient()
        self.coll = self.client[dbName][collName]
        if maskPath is None:
            self.wordCloud = WordCloud(font_path=fontPath, width=400, height=400, max_words=100)
        else:
            self.mask = np.array(Image.open(maskPath))
            self.wordCloud = WordCloud(font_path=fontPath, mask=self.mask, max_words=100)

        if not os.path.exists(self.imgDir):
            os.mkdir(self.imgDir)
        logging.info('GroupTagCloud connected to MongoDB.')

    def process(self, msg, type):
        shallRunObj = self.isRun(msg, type)
        if shallRunObj['shallRun']:
            destinationChatroomId = msg['FromUserName'] if re.search('@@', msg['FromUserName']) else msg['ToUserName']
            if shallRunObj['key'] is None:
                logging.info('Generating tag cloud for {0}.'.format(shallRunObj['groupName']))
                fn = self.generateTagCloudForGroup(shallRunObj['groupName'], shallRunObj['userName'])
                logging.info('Sending tag cloud file {0} to {1}.'.format(fn, destinationChatroomId))
                itchat.send('@img@{0}'.format(fn), destinationChatroomId)
            else:
                logging.info(shallRunObj['key'])
                if shallRunObj['key'] == 'cat':
                    imgUrl = 'http://lorempixel.com/400/200/cats/'
                elif shallRunObj['key'] == 'food':
                    imgUrl = 'http://lorempixel.com/400/200/food/'
                elif shallRunObj['key'] == 'dog':
                    url = 'http://random.dog/'
                    html = urlopen(url)
                    soup = BeautifulSoup(html.read(), 'html.parser')
                    img = soup.find('img')
                    imgUrl = url + str(img['src'])
                elif shallRunObj['key'] == 'bing':
                    url = 'http://www.bing.com/HPImageArchive.aspx?format=js&idx=0&n=1'
                    with urlopen(url) as f:
                        data = f.read()
                    img = data.decode('utf-8')
                    img = json.loads(img)
                    imgUrl = 'http://www.bing.com' + img['images'][0]['url']
                fn = generateTmpFileName(self.imgDir)
                urlretrieve(imgUrl, fn)
                itchat.send('@img@{0}'.format(fn), destinationChatroomId)

    # Generate a tag cloud image from the latest self.recordMaxNum images. Return the file name.
    def generateTagCloudForGroup(self, groupName, userName=None):
        records = None
        if userName is None:
            records = self.coll.find({'to': groupName}).sort([('timestamp',DESCENDING)]).limit(self.recordMaxNum)
        else:
            records = self.coll.find({'from': userName, 'to': groupName}).sort([('timestamp', DESCENDING)]).limit(self.recordMaxNum)
        texts = [r['content'] for r in records]
        frequencies = Counter([w for text in texts for w in jieba.cut(text, cut_all=False) if len(w) > 1])
        frequencies = {k: min(self.maxFrequency, frequencies[k]) for k in frequencies}
        img = self.wordCloud.generate_from_frequencies(frequencies).to_image()
        fn = generateTmpFileName(self.imgDir)
        img.save(fn)
        return fn

    def isRun(self, msg, type):
        if type != TEXT or 'Content' not in msg:
            return {'shallRun': False}
        if re.search(r'^\s*/tagcloud$', msg['Content']):
            return {'shallRun': True, 'key': None, 'userName': None, 'groupName': msg['User']['NickName']}
        if re.search(r'^\s*/tag$', msg['Content']):
            return {'shallRun': True, 'key': None, 'userName': msg['ActualNickName'], 'groupName': msg['User']['NickName']}
        if re.search(r'^\s*/cat$', msg['Content']):
            return {'shallRun': True, 'key': 'cat'}
        if re.search(r'^\s*/dog$', msg['Content']):
            return {'shallRun': True, 'key': 'dog'}
        if re.search(r'^\s*/food$', msg['Content']):
            return {'shallRun': True, 'key': 'food'}
        if re.search(r'^\s*/bing', msg['Content']):
            return {'shallRun': True, 'key': 'bing'}
        return {'shallRun': False}

# if __name__ == '__main__':
#     groupTagCloud = GroupTagCloud()
#     groupTagCloud.generateTagCloudForGroup('TestGroup')