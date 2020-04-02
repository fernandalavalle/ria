import scrapy


headers = ["city", "state", "studio name", "address", "joined", "dedicated desk (day)", "dedicated desk (week)", "dedicated desk (month)", "dedicated desk  (year)", 
            "hot desk (day)", "hot desk  (week)", "hot desk (month)", "hot desk (year)", 
            "private office (day)", "private office (week)", "private office (month)", "private office (year)"]

class DeskPriceSpider(scrapy.Spider):
    name = "desk_price"

    def start_requests(self):
        urls = [
            'https://www.coworker.com/united-states/massachusetts/boston/staples-studio',
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        row = []
        page = response.url.split("/")
        row[page[5], page[4], page[6], ]
        print('\n')
        print('\n')        
        print(page)
        print('\n')
        print('\n')

        # filename = 'prices-%s.html' % page
        # sections = response.xpath('//div[@class="col-xs-12 pad_none pricing-section-space-outer-6-11-18"]')
        # for price in sections.xpath('//div[@class="col-xs-12 pad_none pricing-section-space-outer-6-11-18"]'):
        #     print('\n')
        #     print('\n')
        #     print(price.extract())
        #     print(price.xpath('.//option[@data-details]').get())
        #     print('\n')
        #     print('\n')
            # collected[price.xpath('//div[@class="col-xs-12 pad_none pricing-section-space-outer-6-11-18"]/h4') = price.xpath('//div[@class="col-xs-12 pad_none pricing-section-space-outer-6-11-18"]/options[@data-details]')

        # print('\n')
        # print('\n')
        # print(collected)
        # print('\n')
        # print('\n')

        with open(filename, 'wb') as f:
            f.write(response.body)
        self.log('Saved file %s' % filename)