# -*- coding: utf-8 -*-
import scrapy


class DomSpiderSpider(scrapy.Spider):

    name = 'dom_spider'
    allowed_domains = ['www.otodom.pl']
    start_urls = ['https://www.otodom.pl/sprzedaz/dom/gdansk/']


    def parse(self, response):
        self.log("This is what I look for: " + response.url)
        for each in response.css('.col-md-content article'):
            item = {
                'title': each.css(".offer-item-title ::text").extract_first().strip(),
                'subtitle': each.css(".offer-item-header p ::text").extract_first().strip(),
                'price': each.css(".offer-item-price ::text").extract_first().strip(),
                'area': each.css(".offer-item-area ::text").extract_first().strip(),
                'link': each.css(".offer-item-header a::attr(href)").extract_first(),

            }
            yield item

            #follow pagination Link
            next_page_url = response.css('li.pager-next a::attr(href)').extract_first()
            if next_page_url:
                next_page_url = response.urljoin(next_page_url)
                yield scrapy.Request(url=next_page_url, callback=self.parse)
