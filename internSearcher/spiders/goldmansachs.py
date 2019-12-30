# -*- coding: utf-8 -*-
import scrapy
from internSearcher.items import Vacancy
from scrapy import Request
import json
from datetime import datetime


class GoldmansachsSpider(scrapy.Spider):
    name = 'goldmansachs'
    allowed_domains = ['www.goldmansachs.com']
    start_urls = ['https://www.goldmansachs.com/careers/students/programs/programs-list.json']

    def parse(self, response):
        data = json.loads(response.text)

        print(data['programs'])
