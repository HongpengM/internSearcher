# -*- coding: utf-8 -*-
import scrapy
from internSearcher.items import Vacancy
from scrapy import Request
import json
from datetime import datetime
from lxml import html, etree
from functools import reduce


class MorganstanleySpider(scrapy.Spider):
    name = 'morganstanley'
    allowed_domains = ['tal.net']
    #start_urls = ['https://morganstanley.tal.net/vx/lang-en-GB/mobile-0/brand-2/xf-3786f0ce9359/candidate/jobboard/vacancy/1/adv/?start=0']

    def start_requests(self):
        urls = {
            'americas': 'https://morganstanley.tal.net/vx/lang-en-GB/mobile-0/brand-2/xf-3786f0ce9359/candidate/jobboard/vacancy/1/adv/?f_Item_Opportunity_13857_lk=747&submitted_via_ajax=true',
            'emea': 'https://morganstanley.tal.net/vx/lang-en-GB/mobile-0/brand-2/xf-3786f0ce9359/candidate/jobboard/vacancy/1/adv/?f_Item_Opportunity_13857_lk=747&submitted_via_ajax=true',
            'asia': 'https://morganstanley.tal.net/vx/lang-en-GB/mobile-0/brand-2/xf-3786f0ce9359/candidate/jobboard/vacancy/1/adv/?f_Item_Opportunity_13857_lk=747&submitted_via_ajax=true',
            'japan': 'https://morganstanley.tal.net/vx/lang-en-GB/mobile-0/brand-2/xf-3786f0ce9359/candidate/jobboard/vacancy/1/adv/?f_Item_Opportunity_13857_lk=747&submitted_via_ajax=true'
        }
        for k in list(urls.keys()):
            yield Request(url=urls[k],
                          meta={'region': k},
                          dont_filter=True)
    def parse(self, response):
        tree = html.fromstring(response.text)
        urls = tree.xpath('//table[@class="table solr_search_list"]/tbody/tr/td/a')
        for url in urls:
            yield Request(url = url.attrib['href'],
                          meta=response.meta,
                          callback=self.parse_vacancy)

            
    def parse_vacancy(self, response):

        tree = html.fromstring(response.text)
        title = tree.xpath('//h1[@class="section"]')
        table = tree.xpath('//div[label]')
        itemData = {}
        for t in table:
            label = t.xpath('label/span')[0].text.lower()
            value = reduce(lambda x, y: str(x).strip() + str(y).strip() , map(lambda x: x.text_content(), t.xpath('div/div')))
            itemData[label] = value
        item = Vacancy()

        '''
        {
        'City': 'New York',
        'Education Level': "Bachelor's Degree, Master's Degree",
        'Business Unit': 'Technology',
        'Job description': 'Morgan Stanley believes capital has the power to create positive change in the world. ...',
        'Job Level': 'Intern',
        'Program': 'Summer Analyst'
        }
        '''
        item['employer'] = 'Morgan Stanley'
        item['region'] = response.meta['region']
        item['title'] = title[0].text
        item['cities'] = [itemData['city']]
        item['education'] = itemData['education level']
        item['businessUnit'] = itemData['business unit']
        item['jd'] = itemData['job description']
        item['links'] = response.request.url
        if 'internship' in itemData['program'].lower() or 'summer' in itemData['program'].lower() or 'off-cycle' in itemData['program'].lower() :
            item['pType'] = itemData['program']
            item['collections'] = 'Intern'
            item['otherKeyInfo'] = {'jobLevel': itemData['job level']}
        elif 'full' in itemData['program'].lower():
            item['pType'] = itemData['program']
            item['collections'] = 'Fulltime'
            item['otherKeyInfo'] = {'jobLevel': itemData['job level']}
        else:
            item['pType'] = itemData['program']
            item['collections'] = 'Fulltime'
            item['otherKeyInfo'] = {'jobLevel': itemData['job level']}
            
        yield item
