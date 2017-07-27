from pymongo import MongoClient, DESCENDING
from utilities import *
from ProcessInterface import ProcessInterface
import numpy as np
from PIL import Image
from wordcloud import WordCloud
import itchat
from itchat.content import *
import jieba
from collections import Counter
import gensim
import itertools

class GroupTagCloud(ProcessInterface):
    recordMaxNum = 500
    maxFrequency = 40
    imgDir = 'Temp'

    def __init__(self, maskPath = None):
        # self.coll = DbClient[dbName][collName]
        if maskPath is None:
            self.wordCloud = WordCloud(font_path=FontPath, width=500, height=500, max_words=100)
        else:
            self.mask = np.array(Image.open(maskPath))
            self.wordCloud = WordCloud(font_path=FontPath, mask=self.mask, max_words=100)

        logging.info('GroupTagCloud connected to MongoDB.')

    def process(self, msg, type):
        if type != TEXT:
            return

        shallRunObj = self.isRun(msg, type)
        if shallRunObj['shallRun']:
            toLog = 'Generating tag cloud for {0}.'.format(shallRunObj['groupName'])
            if shallRunObj['userName']:
                toLog = '{0} Username {1}.'.format(toLog, shallRunObj['userName'])
            logging.info(toLog)
            fn = self.generateTagCloudForGroupV2(shallRunObj['groupName'], shallRunObj['userName'])
            group_id = get_group_id(msg)
            logging.info('Sending tag cloud file {0} to {1}.'.format(fn, group_id))
            itchat.send('@img@{0}'.format(fn), group_id)

            # Generate a tag cloud image from the latest self.recordMaxNum records, based on TF-IDF. Return the file name.

    def generateTagCloudForGroupV2(self, groupName, userName=None):
        records = None
        if userName is None:
            records = HisColl.find({'to': groupName, 'type': TEXT}).sort([('timestamp', DESCENDING)]).limit(self.recordMaxNum)
            allRecords = HisColl.find({'to': {'$ne': groupName}, 'type': TEXT}).sort([('timestamp', DESCENDING)]).limit(
                self.recordMaxNum * 5)
            allRecordsGroup = sorted(allRecords, key=lambda x: x['to'])
        else:
            records = HisColl.find({'from': userName, 'to': groupName, 'type': TEXT}).sort([('timestamp', DESCENDING)]).limit(
                self.recordMaxNum)
            allRecords = HisColl.find({'from': {'$ne': userName}, 'to': groupName, 'type': TEXT}).sort(
                [('timestamp', DESCENDING)]).limit(self.recordMaxNum * 5)
            allRecordsGroup = sorted(allRecords, key=lambda x: x['from'])
        docThisGroup = list(jieba.cut(' '.join([r['content'] for r in records])))  # remove the image records
        allRecordsGroup = itertools.groupby(allRecordsGroup, lambda x: x['to'])
        docsOtherGroups = [
            list(jieba.cut(' '.join([r['content'] for r in list(g)])))
            for k, g in allRecordsGroup]
        docs = [docThisGroup] + docsOtherGroups
        dictionary = gensim.corpora.Dictionary(docs)
        docs = [dictionary.doc2bow(doc) for doc in docs]
        id2token = {v: k for k, v in dictionary.token2id.items()}
        tfidf = gensim.models.tfidfmodel.TfidfModel(corpus=docs)
        tagCloudFrequencies = {id2token[x[0]]: x[1] for x in tfidf[docs[0]]}

        img = self.wordCloud.generate_from_frequencies(tagCloudFrequencies).to_image()
        fn = generateTmpFileName(self.imgDir)
        img.save(fn)
        return fn

    # Generate a tag cloud image from the latest self.recordMaxNum images. Return the file name.
    def generateTagCloudForGroup(self, groupName, userName=None):
        records = None
        if userName is None:
            records = HisColl.find({'to': groupName}).sort([('timestamp', DESCENDING)]).limit(self.recordMaxNum)
        else:
            records = HisColl.find({'from': userName, 'to': groupName}).sort([('timestamp', DESCENDING)]).limit(self.recordMaxNum)
        texts = [r['content'] for r in records if r['type'] == TEXT]
        frequencies = Counter([w for text in texts for w in jieba.cut(text, cut_all=False) if len(w) > 1])
        frequencies = {k: min(self.maxFrequency, frequencies[k]) for k in frequencies}
        img = self.wordCloud.generate_from_frequencies(frequencies).to_image()
        fn = generateTmpFileName(self.imgDir)
        img.save(fn)
        return fn

    def isRun(self, msg, type):
        if type != TEXT or 'Content' not in msg:
            return {'shallRun': False}
        if msg['Content'] == '/tagcloud':
            return {'shallRun': True, 'userName': None, 'groupName': msg['User']['NickName']}
        if msg['Content'] == '/tag':
            return {'shallRun': True, 'userName': msg['ActualNickName'], 'groupName': msg['User']['NickName']}
        return {'shallRun': False}
