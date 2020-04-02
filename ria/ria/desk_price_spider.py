import scrapy


class DeskPriceSpider(scrapy.Spider):
    name = "desk_price"

    def start_requests(self):
        urls = [
            'https://www.coworker.com/united-states/massachusetts/boston/staples-studio',
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        print(response)
        page = response.url.split("/")[-2]
        print(page)
        filename = 'prices-%s.html' % page
        with open(filename, 'wb') as f:
            f.write(response.body)
        self.log('Saved file %s' % filename)