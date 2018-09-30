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

from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec


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
        if request.meta['use_selenium'] == True:
            try:
                self.d.get(request.url)
                self.d.maximize_window()
            except TimeoutException as e:            
                print "Timeout Exception."

            if spider.name == "gmail_sender":
                # Opend login window
                compose_elem = self.login_google("zz@gmail.com","zz")
                if compose_elem:
                    print "Login Successed!!"
                else:
                    print "Login Failed."

            resp = TextResponse(url=self.d.current_url,
                                body=self.d.page_source,
                                encoding='utf-8')
            resp.request = request.copy()
            #self.d.quit()
            return resp

    def login_google(self, email, password):
        email_edit  = self.d.find_element_by_xpath('//*[@type="email"]')
        next_id_button = self.d.find_element_by_xpath('//*[@id="identifierNext"]')
        if email_edit and next_id_button:
            email_edit.click()
            email_edit.send_keys(email)
            next_id_button.click()

            pw_elem = WebDriverWait(self.d, 30).until(ec.visibility_of_element_located((By.XPATH, '//*[@type="password"][not(@id)]')))
            pw_elem.click()
            pw_elem.send_keys(password)
            next_pw_button = self.d.find_element_by_xpath('//*[@id="passwordNext"]')
            next_pw_button.click()

            print "Wait ..."
            try:
                compose_elem = WebDriverWait(self.d, 40).until(ec.visibility_of_element_located((By.XPATH, '//*[contains(text(),"Compose")]')))
            except TimeoutException:
                print "Timed out waiting for page to load."
                return None
            else:
                return compose_elem


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