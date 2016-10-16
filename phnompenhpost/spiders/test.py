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
# encoding=utf8
import sys

reload(sys)
sys.setdefaultencoding('utf8')

class TestSpider(CrawlSpider):
    name = "phnompenhpost"
    allowed_domains = ["postkhmer.com"]
    start_urls = [
    'http://www.postkhmer.com/ព័ត៌មានជាតិ',
    ]

    def parse(self, response):

        # decoded = str(response.body).encode('utf-8')  #(type <unicode>)
        # my_code = unicode(response.body, 'utf-8')
        # print('type ==> ', type(my_code))
        # my_ascii = my_code.encode('utf-8')
        # print('ascii type ==> ', type(my_ascii))
        #turn it back into a string, using utf-8 encoding.
        # goodXML = decoded.encode('utf-8')   #(type <str>)
        # print('good', goodXML)

        # response = HtmlResponse(response.url,
        #     encoding='utf-8',
        #     body=urllib.unquote(response.body),
        # )
        # print(response.body)
        # print('responsetext', response.text)
        # HtmlResponse.replace(c_body)
        # print('response1 ===================> ', response)
        # hres = HtmlResponse('http://www.postkhmer.com/ព័ត៌មានជាតិ', body=response.text)
        # print('response1 xpath', response1)
        # url = 'http://www.postkhmer.com/%E1%9E%96%E1%9F%90%E1%9E%8F%E1%9F%8C%E1%9E%98%E1%9E%B6%E1%9E%93%E1%9E%87%E1%9E%B6%E1%9E%8F%E1%9E%B7'
        # html_response = urllib.unquote(response).decode('utf8')
        # URL = 'http://www.postkhmer.com/ព័ត៌មានជាតិ'
        # url_handler = urllib2.build_opener()
        # urllib2.install_opener(url_handler)
        # handle = url_handler.open(URL)
        # response = handle.read()
        # handle.close()
        # print('response1', type(unicode(response, 'utf-8')))
        # html_response = HtmlResponse(URL, body=response)
        # print('response2 html_response===> ', html_response)
        # hxs = scrapy.Selector(html_response)
        # response2 = hxs.xpath('//div[@class="category"]')
        # print('response2 xpath ==> ', response2)
        # hxs = scrapy.Selector(html_response)

        now = time.strftime('%Y-%m-%d %H:%M:%S')
        # hxs = scrapy.Selector(response)
        # desc = hxs.xpath('//div[@class="block-49"]/div[@class="category"]')
        # print desc

        # testlen = hxs.xpath('//div[@class="block-49"]/div[@class="category"]')
        # print(testlen)
        # print('1', testlen)
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
            item['description'] = description.xpath('strong[1]/text()').extract_first() + ' ' + description.xpath('text()').extract_first()

        imageUrl = article.xpath("""
            a[1]/img[1]/@src
            """)

        if not imageUrl:
            print('Phnompenhpost => [' + now + '] No imageUrl')
        else:
            item['imageUrl'] = imageUrl.extract_first()

        yield item

        articles = hxs.xpath('//div[@class="category"]')
        for myart in articles[1:]:
            item = PhnompenhpostItem()
            item['categoryId'] = '1'
            name = myart.xpath('h3[1]/a[1]/text()')
            if not name:
                print('Phnompenhpost => [' + now + '] No title')
            else:
                item['name'] = name.extract_first()
            print item['name']

            url = myart.xpath('h3[1]/a[1]/@href')
            if not url:
                print('Phnompenhpost => [' + now + '] No url')
            else:
                item['url'] = 'http://www.postkhmer.com' + url.extract_first()
            print item['url']

            description = myart.xpath('h3[1]/following-sibling::div[@class="summary"][1]/p[1]')
            if not description:
                print('Phnompenhpost => [' + now + '] No description')
            else:
                item['description'] = description.xpath('strong/text()').extract_first() + ' ' + description.xpath('text()').extract_first()
            print item['description']

            imageUrl = myart.xpath("""
                div[@class="article-image"]/a[1]/img[1]/@src
                """)
            if not imageUrl:
                print('Phnompenhpost => [' + now + '] No imageUrl')
            else:
                item['imageUrl'] = imageUrl.extract_first()

            yield item

        def parse_detail(self, response):
            item = response.meta['item']
            hxs = scrapy.Selector(response)
            now = time.strftime('%Y-%m-%d %H:%M:%S')

            item_page = hxs.css('div.item-page')
            description = item_page.xpath('p[1]/text()')
            if not description:
                print('Phnompenhpost => [' + now + '] No description')
            else:
                item['description'] = item_page.xpath('p[1]/strong/text()').extract_first() + ' ' + description.extract_first()

                imageUrl = item_page.xpath('p[last()]/img/@src')
                if not imageUrl:
                    print('Phnompenhpost => [' + now + '] No imageUrl')
                else:
                    item['imageUrl'] = imageUrl.extract_first()


                    yield item
