# -*- coding: utf-8 -*-
import scrapy
from scrapy.exceptions import CloseSpider
from scrapy import Request

from urlparse import urlparse
from json import loads
from datetime import datetime, time
from collections import OrderedDict
import os,re
import urllib
import requests
from scrapy.utils.response import open_in_browser

#post_class = re.findall(r'</div><div id=\"u_0_[\w]+\"><div class=\"_[\w]+\"><div class=\"(_[\w\-_]+\s+_[\w\-_]+?)\">', response.body)

class GmailSpider(scrapy.Spider):
	name = "gmail_sender"

	start_urls = (
					'http://gmail.com/',
					)

	def start_requests(self):
		for url in self.start_urls:
			yield Request(url, callback=self.parse, meta={'use_selenium':True})

	def parse(self, response):
		print "##############"
		print response.url