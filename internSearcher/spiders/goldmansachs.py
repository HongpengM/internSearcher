# -*- coding: utf-8 -*-
import scrapy
from internSearcher.items import Vacancy
from scrapy import Request
import json
from datetime import datetime

import logging
logger = logging.getLogger('** Goldman Sachs Spider Logger **')

def gsPrograms(pType):
    pTypeDict = {
        '...an internship.': 'internship',
        '...a full-time position.': 'full-time',
        '...exploratory programs.': 'exploratory programs'
    }
    if pType in list(pTypeDict.keys()):
        return pTypeDict[pType]
    else:
        return 'Other'

class GoldmansachsSpider(scrapy.Spider):
    name = 'goldmansachs'
    allowed_domains = ['www.goldmansachs.com']
    start_urls = ['https://www.goldmansachs.com/careers/students/programs/programs-list.json']

    def parse(self, response):
        data = json.loads(response.text)
        
        for d in data['programs']:
            item = Vacancy()
            
            item['title'] = d['title']
            item['employer'] = 'Goldman Sachs'
            item['region'] = d['region']['geoTag']
            item['cities'] = d['cities']
            item['jd'] = str(d['eligibility']).replace('\r','').replace('\n','') + '\n' + str(d['programTypeDescription']).replace('\r','').replace('\n','')#
            #.replace('\r','').replace('\n','') \
            item['links'] = 'https://www.goldmansachs.com' + d['url']
            item['pType'] = list(map(lambda x: gsPrograms(x['name']),
                                     d['programType']))
            if  'full-time' in item['pType']:
                item['collections'] = 'Fulltime'
            elif 'internship' in item['pType']  or  'exploratory programs' in item['pType']:
                item['collections'] = 'Intern'
            else:
                item['collections'] = 'Other'
            yield item
        #for prog in range(len(data['programs'])):

        #    logger.info(str(prog)+'\n', data['programs'][prog])
            
