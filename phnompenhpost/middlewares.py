from scrapy.http import HtmlResponse
from scrapy.utils.python import to_bytes
from selenium import webdriver
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from pyvirtualdisplay import Display
from scrapy import signals
from xvfbwrapper import Xvfb

class SeleniumMiddleware(object):

    @classmethod
    def from_crawler(cls, crawler):
        middleware = cls()
        #display = Display(visible=0, size=(800, 600))
        #display.start()
        crawler.signals.connect(middleware.spider_opened, signals.spider_opened)
        crawler.signals.connect(middleware.spider_closed, signals.spider_closed)
        #display.stop()
        return middleware

    def process_request(self, request, spider):
        request.meta['driver'] = self.driver  # to access driver from response
        self.driver.get(request.url)
        body = to_bytes(self.driver.page_source)  # body must be of type bytes
        return HtmlResponse(self.driver.current_url, body=body, encoding='utf-8', request=request)

    def spider_opened(self, spider):
        # self.driver = webdriver.Chrome("/usr/lib/chromium-browser/chromedriver")
        #firefox_capabilities = DesiredCapabilities.FIREFOX
        #firefox_capabilities['marionette'] = True
        #firefox_capabilities['binary'] = '/usr/local/bin/geckodriver'
        # self.driver = webdriver.Firefox(capabilities=firefox_capabilities)
        # self.driver = webdriver.Firefox()
        self.driver = webdriver.PhantomJS()
        self.driver.set_window_size(1120, 550)

    def spider_closed(self, spider):
        self.driver.close()
