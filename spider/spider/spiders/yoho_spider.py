# -*- coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

import scrapy
from spider.items import YohoItem
import datetime

categories = [u'上衣', u'裤装']

class YohoSpider(scrapy.Spider):
    name = "yoho"
    allowed_domains = ["yohobuy.com"]
    start_urls = [
            "http://guang.yohobuy.com/Index/index?type=2&page=1",
    ]


    def parse(self, response):
        today_str =  datetime.datetime.now().strftime('%Y-%m-%d')
        today = datetime.datetime.strptime(today_str, '%Y-%m-%d')
        for li in response.css("div.msg-list > div.msg-content" ):
            href = li.xpath("div[@class='msg-img']/a/@href")
            match_id = li.xpath("@data-id").extract_first()
            match_createdAt = li.xpath("div[@class='msg-info']/p[@class='msg-app']/span[@class='publish-time']/text()").extract()[1].strip().replace('\t','').replace('\r','').replace('\n', '')
            match_createdAt = datetime.datetime.strptime(match_createdAt.split(' ')[0].encode('UTF-8'), '%Y年%m月%d日')
            # if match_createdAt < today:
                # continue
            match_tags = li.xpath("div[@class='msg-info']/div[@class='footer']/div[@class='tags']/a/text()").extract()
            matching = {'id': match_id, 'tags':match_tags, 'createdAt': match_createdAt}
            url = response.urljoin(href.extract_first())
            yield scrapy.Request(url, meta={'matching':matching},callback=self.parse_matching_list)
            print '%s ok!'%match_id
            next_page = response.xpath("//a[@title='"+u'下一页'+"']/@href").extract_first()
            if next_page:
                next_page_url = response.urljoin(next_page)
                yield scrapy.Request(next_page_url, self.parse)

    def parse_matching_list(self, response):
        for href in response.css("div.related-reco.block > div.recos div.good-info a::attr('href')"):
            url = response.urljoin(href.extract())
            yield scrapy.Request(url, meta={'matching':response.meta['matching']}, callback=self.parse_closing)

    def parse_closing(self, response):
        # 限定获得男装
        is_boys = response.xpath("//p[@class='path-nav']/a[1]/text()").extract_first() == u'BOYS首页'
        if is_boys is False:
            return
        matching = response.meta['matching']
        # 限定上装或者裤装
        category = response.xpath("//p[@class='path-nav']/a[2]/text()").extract_first()
        if category not in categories:
            return
        item = YohoItem()
        item['matching'] = matching
        item['category'] = category
        item['img_url'] = response.xpath("//img[@id='img-show']/@src").extract_first()
        item['product_url'] = response.url
        item['style'] = response.xpath("//p[@class='path-nav']/a[3]/text()").extract_first()
        yield item
