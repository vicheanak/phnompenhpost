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
