import scrapy


headers = ["country", "city", "state", "studio name", "address", "joined", 
            "private office (day)", "private office (week)", "private office (month)", "private office (year)",
            "dedicated desk (day)", "dedicated desk (week)", "dedicated desk (month)", "dedicated desk  (year)", 
            "hot desk (day)", "hot desk  (week)", "hot desk (month)", "hot desk (year)"]

class DeskPriceSpider(scrapy.Spider):
    name = "desk_price"

    def start_requests(self):
        urls = [
            'https://urldefense.proofpoint.com/v2/url?u=https-3A__www.coworker.com_united-2Dstates_massachusetts_boston_staples-2Dstudio&d=DwIGAg&c=P1Dci1wcau9HQxzdgeFbIQ&r=0u6hkQecOH0ct0Wg0xHRibYs5aF62OB8g9ssYaZsiu4&m=5zEjfI3ZD0nfuPZxs1dvmhS8-gwIJYjbmn1-wSxXXwE&s=OvQdjywtdBgmAslBNDiWAJMLwUXi5zUMVPVtiiEhdwE&e= ',
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        row = []
        page = response.url.split("/")
        print('\n')
        print('\n')        
        print(page)
        print('\n')
        print('\n')

        row.append(page[3])
        row.append(page[5])
        row.append(page[4])
        row.append(page[6])

        print(row[0])
        print(row[1])
        print(row[2])
        print(row[3])
        print('\n')
        print('\n')


        # Add address
        address = response.xpath('//div[@class="col-xs-12 pade_none muchroom_mail"]').getall()

        print(len(address))
        print(address)
        print(type(address[0]))
        start=(address[0].index("/i> ")+4)
        end=address[0].index("</div>")
        print('\n')
        print('\n')
        address_only=address[0][start:end:]
        print(address_only)
        print('\n')
        print('\n')
        row.append(address_only)
        print(row)

        # Add Join date
        joined = response.xpath('//div[@class="date_joined_rs"]').getall()
        print('\n')
        print('\n')
        print(len(joined))
        print(joined)

        print(type(joined[0]))
        start=(joined[0].index("Joined ")+7)
        end=joined[0].index("</span>")
        print('\n')
        print('\n')
        joined_only=joined[0][start:end:]
        print(joined_only)
        print('\n')
        print('\n')
        row.append(joined_only)
        print(row)

        # Prices
        # "private office (day)", "private office (week)", "private office (month)", "private office (year)",
        # "dedicated desk (day)", "dedicated desk (week)", "dedicated desk (month)", "dedicated desk  (year)", 
        # "hot desk (day)", "hot desk  (week)", "hot desk (month)", "hot desk (year)"]
        filename = 'prices-%s.html' % page[6]
        sections = response.xpath('//div[@class="col-xs-12 pad_none pricing-section-space-outer-6-11-18"]').getall()
        print('\n')
        print('\n')
        print(len(sections))
        print(sections[0])
        print('\n')
        print('\n')
        print(sections[1])
        print('\n')
        print('\n')
        print(sections[2])
        print('\n')
        print('\n')


        start=(address[0].index("/i> ")+4)
        end=address[0].index("</div>")
        print('\n')
        print('\n')
        address_only=address[0][start:end:]
        print(address_only)
        print('\n')
        print('\n')
        row.append(address_only)
        print(row)

        po_day =""
        po_week = ""
        po_month = ""
        po_year = ""
        dd_day = ""
        dd_week = ""
        dd_month = ""
        dd_year = ""
        hd_day = ""
        hd_week = ""
        hd_month = ""
        hd_year = ""

        if "empty-message" not in sections[0]: 
            if sections[0].find(Private Office)!=-1:
                end=0
                if end<len(sections[0]):
                    start = sections[0].index('<option data-details='{"price":"')
                    print(start)
                    end= sections[0].index("</option>")
                    print(end)
                    subsec=sections[0][start:end:]

                    po_day =

                    po_week = 

                    po_month =

                    po_year = 

        dd_day = 

        dd_week = 

        dd_month = 

        dd_year = 

        hd_day = 

        hd_week = 

        hd_month = 

        hd_year = 

        sections2=response.xpath('//div[@class="col-xs-12 pad_none pricing-section-space-outer-6-11-18"]')
        print("hey")
        prices=sections2.xpath('.//option[@data-details]').getall()
        print(len(prices))
        print("hello")
        for i in range(len(prices)):
            print('\n')
            print(prices[i])
        

        # print(prices)

        # for price in sections2.xpath('//div[@class="col-xs-12 pad_none pricing-section-space-outer-6-11-18"]'):
        #     print("a")
            # print('\n')
            # print('\n')
            # print(price.extract())
            # print("b")
            # print('\n')
            # print('\n')
            # print(price.xpath('.//option[@data-details]').get())
            # print("c")
            # print('\n')
            # print('\n')
        #     collected=price.xpath('//div[@class="col-xs-12 pad_none pricing-section-space-outer-6-11-18"]/h4') = price.xpath('//div[@class="col-xs-12 pad_none pricing-section-space-outer-6-11-18"]/options[@data-details]').getall()

        # print('\n')
        # print('\n')
        # print(collected)
        # print('\n')
        # print('\n')

        # sections = response.xpath('//div[@class="col-xs-12 pad_none pricing-section-space-outer-6-11-18"]')
        # for price in sections.xpath('//div[@class="col-xs-12 pad_none pricing-section-space-outer-6-11-18"]'):
        #     print('\n')
        #     print('\n')
        #     print(price.extract())
        #     print(price.xpath('.//option[@data-details]').get())
        #     print('\n')
        #     print('\n')
        #     collected[price.xpath('//div[@class="col-xs-12 pad_none pricing-section-space-outer-6-11-18"]/h4') = price.xpath('//div[@class="col-xs-12 pad_none pricing-section-space-outer-6-11-18"]/options[@data-details]')

        # print('\n')
        # print('\n')
        # print(collected)
        # print('\n')
        # print('\n')

        with open(filename, 'wb') as f:
            f.write(response.body)
        self.log('Saved file %s' % filename)