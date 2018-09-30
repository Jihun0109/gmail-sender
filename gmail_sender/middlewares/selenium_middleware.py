from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException

from scrapy.http import TextResponse
from scrapy.exceptions import CloseSpider
from scrapy import signals
from PIL import Image
import time
import os
import urllib
from operator import itemgetter
from datetime import datetime

class SeleniumMiddleware(object):

    def __init__(self, s):
        self.exec_path = s.get('CHROME_PATH', './phantomjs.exe')

###########################################################

    @classmethod
    def from_crawler(cls, crawler):
        obj = cls(crawler.settings)

        crawler.signals.connect(obj.spider_opened,
                                signal=signals.spider_opened)
        crawler.signals.connect(obj.spider_closed,
                                signal=signals.spider_closed)
        return obj

###########################################################

    def spider_opened(self, spider):
        print "STARTTTTTTTTTTTTTTTTTTTTTTTTT"
        try:
            self.d = init_driver("chromedriver.exe")
        except TimeoutException:
            CloseSpider('PhantomJS Timeout Error!!!')
        
###########################################################

    def spider_closed(self, spider):
        try:
            self.d.quit()
        except:
            pass
###########################################################
    
    def process_request(self, request, spider):
        print "#############################################"
        print "#############################################"
        print "#### Received url request from scrapy #######"
        print "#############################################"
        print "#############################################"
        print request.url
        if request.meta['use_selenium'] == True:
        #print request.meta
            #self.d = init_driver("")
            
            try:
                self.d.get(request.url)
            except TimeoutException as e:            
                print "Timeout Exception."

            resp = TextResponse(url=self.d.current_url,
                                body=self.d.page_source,
                                encoding='utf-8')
            resp.request = request.copy()
            #self.d.quit()
            return resp

###########################################################
###########################################################

def init_driver(path):
    #d = webdriver.PhantomJS(executable_path=path)
    service_log_path = 'chromedriver.log'
    service_args = ['--verbose', '--no-sandbox']
    d = webdriver.Chrome(path, service_args=service_args, service_log_path=service_log_path)

    # fp = webdriver.FirefoxProfile()
    # fp.set_preference("http.response.timeout", 15)
    # fp.set_preference("dom.max_script_run_time", 15)

    # d = webdriver.Firefox()
    # d.set_page_load_timeout(30)

    return d