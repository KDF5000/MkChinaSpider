# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.http import Request

class CompanyinfospiderSpider(scrapy.Spider):
    name = "CompanyInfoSpider"
    allowed_domains = ["http://cn.made-in-china.com/"]
    # link_extractor = LinkExtractor(restrict_xpaths="//label[@class='co-name']")
    page_size = 30
    total_page = 1023
    base_url = "http://cn.made-in-china.com/companysearch.do?propertyValues=&" \
               "action=hunt&senior=0&certFlag=0&order=0&style=b&comProvince=nolimit" \
               "&comCity=&size=30&viewType=&word=%B9%E3%B6%AB&from=hunt&" \
               "comServiceType=&chooseUniqfield=0&page="
    next_page = 1
    start_urls = (
        'http://cn.made-in-china.com/companysearch.do?'
        'propertyValues=&action=hunt&senior=0&certFlag=0'
        '&order=0&style=b&page=1&comProvince=nolimit&'
        'comCity=&size=30&viewType=&word=%B9%E3%B6%AB&'
        'from=hunt&comServiceType=&chooseUniqfield=0',
    )

    def parse(self, response):
        # links = [l for l in self.link_extractor.extract_links(response)]
        co_name_links = response.xpath("//label[@class='co-name']/a")
        for name_a in co_name_links:
            company_name = name_a.xpath('@title').extract()[0]
            company_link = name_a.xpath('@href').extract()[0]
            company_file_url = company_link + "/files-" + company_name + '.html'
            yield Request(url=company_file_url, callback=self.get_company_info, dont_filter=True)
        self.next_page += 1
        if self.next_page <= self.total_page:
            yield Request(url=self.base_url+str(self.next_page), dont_filter=True)

    def parse_page(self, response):
        co_name_links = response.xpath("//label[@class='co-name']/a")
        for name_a in co_name_links:
            company_name = name_a.xpath('@title').extract()[0]
            company_link = name_a.xpath('@href').extract()[0]
            company_file_url = company_link + "/files-" + company_name + '.html'
            yield Request(url=company_file_url, callback=self.get_company_info, dont_filter=True)
        self.next_page += 1
        if self.next_page <= self.total_page:
            yield Request(url=self.base_url+self.next_page, callback=self.parse_page, dont_filter=True)

    def get_company_info(self, response):
        with open(response.url,'w') as f:
            f.write(response.body)
        cert_table_tr = response.xpath("//table[@class='tb-cert']/tr")
        th_list = cert_table_tr.xpath('th/text()').extract()
        td_list = cert_table_tr.xpath('td/text()').extract()

        union_list = zip(th_list, td_list)
        company_info = dict((name.replace("：", "").strip(), value.strip()) for name, value in union_list)












