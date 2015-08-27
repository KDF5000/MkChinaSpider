# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
import json
from RSpider.items import RspiderItem


class CompanyinfoSpider(CrawlSpider):
    name = 'CompanyInfo'
    allowed_domains = []
    start_urls = ["http://cn.made-in-china.com/companysearch.do?"
                  "propertyValues=&action=hunt&senior=0&certFlag=0&"
                  "order=0&style=b&comProvince=nolimit&comCity=&"
                  "size=30&viewType=&word=%%B9%%E3%%B6%%AB&from=hunt"
                  "&comServiceType=&chooseUniqfield=0&page=%s" % i for i in range(1, 1023)]

    rules = (
        Rule(LinkExtractor(restrict_xpaths="//label[@class='co-name']"), follow=True),
        Rule(LinkExtractor(allow=r"files-[A-Z\d%]+.html$", restrict_xpaths="//div[@class='top_nav']"),
             callback='parse_item')
    )

    def parse_item(self, response):
        item = RspiderItem()
        cert_table_tr = response.xpath("//table[@class='tb-cert'][1]//tr")
        th_list = cert_table_tr.xpath('th/text()').extract()
        td_list = cert_table_tr.xpath('td/text()').extract()

        union_list = zip(th_list, td_list)
        company_info = dict((name.replace(u"：", "").strip(), value.strip()) for name, value in union_list)
        item['url'] = response.url
        item['data'] = json.dumps(company_info)
        return item
        # print company_info
        # print '----------------------------'
        # for k, v in company_info.iteritems():
        #     print k, v
        # print 'Length:', len(company_info.keys())
        # print '----------------------------'


