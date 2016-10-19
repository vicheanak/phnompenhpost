# -*- coding: utf-8 -*-
import scrapy
from scrapy.spiders import CrawlSpider, Rule
from phnompenhpost.items import PhnompenhpostItem
from scrapy.linkextractors import LinkExtractor
import time
import urllib
import urllib2
from scrapy.selector import HtmlXPathSelector
from scrapy.http import HtmlResponse
from lxml.html import builder as E
# encoding=utf8
import sys
import lxml.etree
import lxml.html

reload(sys)
sys.setdefaultencoding('utf8')

class TestSpider(CrawlSpider):
    name = "phnompenhpost"
    allowed_domains = ["postkhmer.com"]
    start_urls = [
    'http://www.postkhmer.com/ព័ត៌មានជាតិ',
    ]

    def parse(self, response):

        now = time.strftime('%Y-%m-%d %H:%M:%S')
        response = HtmlResponse(response.url,
            encoding='utf-8',
            body=urllib.unquote(response.body),
        )
        hxs = scrapy.Selector(response)
        article = hxs.xpath('//div[@class="first-item"][1]')
        item = PhnompenhpostItem()
        item['categoryId'] = '1'
        name = article.xpath('h3[1]/a[1]/text()')

        if not name:
            print('Phnompenhpost => [' + now + '] No title')
        else:
            item['name'] = name.extract_first()

        url = article.xpath('h3[1]/a[1]/@href')
        if not url:
            print('Phnompenhpost => [' + now + '] No url')
        else:
            item['url'] = 'http://www.postkhmer.com' + url.extract_first()

        description = article.xpath('following-sibling::div[@class="summary"]/p[1]')
        if not description:
            print('Phnompenhpost => [' + now + '] No description')
        else:
            item['description'] = description.xpath('text()').extract_first()

        imageUrl = article.xpath("""
            a[1]/img[1]/@src
            """)

        item['imageUrl'] = ''
        if not imageUrl:
            print('Phnompenhpost => [' + now + '] No imageUrl')
        else:
            item['imageUrl'] = imageUrl.extract_first()

        request = scrapy.Request(item['url'], callback=self.parse_detail)
        request.meta['item'] = item
        yield request

        articles = hxs.xpath('//div[@class="category"]')
        for myart in articles[1:]:
            item = PhnompenhpostItem()
            item['categoryId'] = '1'
            name = myart.xpath('h3[1]/a[1]/text()')
            if not name:
                print('Phnompenhpost => [' + now + '] No title')
            else:
                item['name'] = name.extract_first()

            url = myart.xpath('h3[1]/a[1]/@href')
            if not url:
                print('Phnompenhpost => [' + now + '] No url')
            else:
                item['url'] = 'http://www.postkhmer.com' + url.extract_first()

            description = myart.xpath('h3[1]/following-sibling::div[@class="summary"][1]/p[1]')
            if not description:
                print('Phnompenhpost => [' + now + '] No description')
            else:
                item['description'] = description.xpath('text()').extract_first()



            request = scrapy.Request(item['url'], callback=self.parse_detail)
            request.meta['item'] = item
            yield request

    def parse_detail(self, response):
        item = response.meta['item']
        hxs = scrapy.Selector(response)
        now = time.strftime('%Y-%m-%d %H:%M:%S')

        print item['url']

        imageUrl = hxs.xpath("""
            //img[@itemprop="contentURL"][1]/@src
            """)
        imageEle = ''
        item['imageUrl'] = ''
        if not imageUrl:
            print('Phnompenhpost => [' + now + '] No imageUrl')
        else:
            imageEle = E.IMG(src=imageUrl.extract_first())
            imageEle = lxml.html.tostring(imageEle, encoding=unicode)
            item['imageUrl'] = imageUrl.extract_first()

        root = lxml.html.fromstring(response.body)
        lxml.etree.strip_elements(root, lxml.etree.Comment, "script", "head")
        htmlcontent = ''

        for p in root.xpath('//div[@id="ArticleBody"][1]'):
            htmlcontent = lxml.html.tostring(p, pretty_print=True, encoding=unicode)

        item['htmlcontent'] = imageEle + htmlcontent

        yield item




