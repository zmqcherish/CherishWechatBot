# -*- coding: utf-8 -*-
from utilities import *
from itchat.content import *
from ProcessInterface import ProcessInterface
from pymongo import DESCENDING
import itchat
import numpy as np
# from matplotlib.font_manager import FontProperties
from matplotlib.dates import HourLocator, DateFormatter
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as pp
from time import time
from datetime import datetime, timedelta
from collections import Counter

class ActivityInfo(ProcessInterface):
    timestampSubtract = 3600 * 24  # 1 day
    maxActivityInfoCount = 10
    imgDir = 'Temp'

    def __init__(self):
        # self.coll = DbClient[dbName][collName]
        # self.prop = FontProperties(fname=FontPath)
        logging.info('ActivityInfo initialized.')

    def process(self, msg, type):
        if type != TEXT:
            return

        if msg['Content'] == '/activity':
            group_id, group_name = get_group_info(msg)
            logging.info('Generating activity info for {0}.'.format(group_name))
            fn = self.generateActivityInfoForGroup(group_name)
            itchat.send_image(fn, group_id)
        elif msg['Content'] == '/myactive':
            group_id, group_name = get_group_info(msg)
            user = msg['ActualNickName']
            logging.info('Generating activity info for {}-{}.'.format(group_name, user))
            fn = self.generateActivityInfoForPerson(group_name, user)
            itchat.send_image(fn, group_id)
            
    def generateActivityInfoForPerson(self, group_name, user):
        hour_data=[0] * 24
        records = list(HisColl.find({'to': group_name, 'from': user}))
        for r in records:
            rtime = datetime.strptime(r['time'], '%Y-%m-%d %H:%M:%S')
            hour = rtime.hour
            hour_data[hour] += 1
        
        n = 24
        x = np.arange(n)
        bar_width = 0.5
        opacity = 1
        pp.figure()
        pp.bar(x, hour_data, bar_width, alpha=opacity, color='#87CEFA')	#, label='发言数量'
        pp.xlabel('小时', fontproperties=FontProp)
        pp.ylabel('数量', fontproperties=FontProp)
        pp.title('{} 发言数24小时统计图'.format(user), fontproperties=FontProp)
        pp.xticks(x, list(range(n)))
        # plt.ylim(0, max(hour_data[2]) * 1.2)
        pp.legend()
        pp.tight_layout()

        fn = generateTmpFileName(self.imgDir)
        pp.savefig(fn)
        return fn

    def generateActivityInfoForGroup(self, group_name):
        timestampYesterday = int(time()) - self.timestampSubtract    #北京时间
        records = list(HisColl.find({'to': group_name, 'timestamp': {'$gt': timestampYesterday}}).sort([('timestamp', DESCENDING)]))
        
        # Get histogram for activity
        hist, bins = np.histogram([x['timestamp'] for x in records], bins=24)
        center = (bins[:-1] + bins[1:]) / 2
        datex = [datetime.fromtimestamp(x) + timedelta(hours=8) for x in center]
        pp.figure(figsize=(6, 16))
        # pp.subplots_adjust(left=0.1, bottom=0.1, right=0.9, top=0.9, wspace=0, hspace=0.5)
        pp.subplots_adjust(bottom=0.05, top=0.95, hspace=0.4)
        ax = pp.subplot(3, 1, 1)
        pp.plot_date(datex, hist, '.-')
        pp.gcf().autofmt_xdate()
        pp.xlabel('时间', fontproperties=FontProp)
        pp.ylabel('每小时消息数', fontproperties=FontProp)
        ax.xaxis.set_major_formatter(DateFormatter('%m-%d %H:%M'))

        # Get bar chart for active users
        self.get_activitydata(records)
        self.get_activitydata2(group_name)

        fn = generateTmpFileName(self.imgDir)
        pp.savefig(fn)
        return fn
    
    def get_activitydata(self, records):
        pieDat = Counter([x['from'] for x in records])
        pieDatSorted = sorted([(k, pieDat[k]) for k in pieDat], key=lambda x: x[1], reverse=True)
        if len(pieDatSorted) > self.maxActivityInfoCount:
            pieDatSorted = pieDatSorted[:self.maxActivityInfoCount]
        ax = pp.subplot(3, 1, 2)
        width = 0.7
        x = np.arange(len(pieDatSorted)) + width
        xText = [xx[0] for xx in pieDatSorted]
        y = [xx[1] for xx in pieDatSorted]
        pp.bar(x, y, width)
        a = pp.gca()
        a.set_xticklabels(a.get_xticks(), {'fontProperties': FontProp})
        pp.xticks(x, xText, rotation='vertical')
        pp.xlabel('用户', fontproperties=FontProp)
        pp.ylabel('24小时消息数', fontproperties=FontProp)
        ax.set_xlim([0, len(xText) + 1 - width])
    
    def get_activitydata2(self, group_name):
        records = list(HisColl.find({'to': group_name}))
        pieDat = Counter([x['from'] for x in records])
        pieDatSorted = sorted([(k, pieDat[k]) for k in pieDat], key=lambda x: x[1], reverse=True)
        if len(pieDatSorted) > self.maxActivityInfoCount:
            pieDatSorted = pieDatSorted[:self.maxActivityInfoCount]
        ax = pp.subplot(3, 1, 3)
        width = 0.7
        x = np.arange(len(pieDatSorted)) + width
        xText = [xx[0] for xx in pieDatSorted]
        y = [xx[1] for xx in pieDatSorted]
        pp.bar(x, y, width)
        a = pp.gca()
        a.set_xticklabels(a.get_xticks(), {'fontProperties': FontProp})
        pp.xticks(x, xText, rotation='vertical')
        pp.xlabel('用户', fontproperties=FontProp)
        pp.ylabel('总消息数', fontproperties=FontProp)
        ax.set_xlim([0, len(xText) + 1 - width])
