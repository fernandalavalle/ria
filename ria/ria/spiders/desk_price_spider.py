import scrapy
import json

ERROR_FILE = "errors.txt"

headers = ["country", "city", "state", "name", "address", "joined", "type of office", "price", "time period"]

class DeskPriceSpider(scrapy.Spider):
    name = "desk_price"

    def start_requests(self):
        urls = [
            'https://urldefense.proofpoint.com/v2/url?u=https-3A__www.coworker.com_united-2Dstates_massachusetts_boston_staples-2Dstudio&d=DwIGAg&c=P1Dci1wcau9HQxzdgeFbIQ&r=0u6hkQecOH0ct0Wg0xHRibYs5aF62OB8g9ssYaZsiu4&m=5zEjfI3ZD0nfuPZxs1dvmhS8-gwIJYjbmn1-wSxXXwE&s=OvQdjywtdBgmAslBNDiWAJMLwUXi5zUMVPVtiiEhdwE&e= ',
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def get_text(self, selector_string): 
        if not selector_string: 
            return selector_string
        if "<" in selector_string: 
            open_tag_right_index = selector_string.index(">")
            close_tag_left_index = selector_string.index("</")
            return selector_string[open_tag_right_index+1:close_tag_left_index]

    def extract_price(self, json_string):
        parsed = json.loads(json_string)
        return parsed["price"]
    
    def handle_one_section(self, section_string): 
        type_of_price=self.get_text(section_string.xpath('.//h4').get())
        time_periods=[self.get_text(x) for x in section_string.xpath('.//option[@data-details]').getall()]
        prices=[ self.extract_price(x) for x in section_string.xpath('.//option/@data-details').getall()]
        no_price = section_string.xpath('.//div/@class="empty-message"').getall()
        
        return {
            "type_of_price" : type_of_price, 
            "time_periods" : time_periods, 
            "prices" : prices
        }


    # Returns: (List of dictionary rows, errors)
    def parse(self, response):
        output_rows = []
        errors = []

        row = {}
        page = response.url.split("/")
        print('\n')
        print('\n')        
        print(page)
        print('\n')
        print('\n')

        
        row["name"] = page[-1]
        row["city"] = page[-2]

        if ("united-states" in page): 
            row["country"] = page[-4]
            row["state"] = page[-3]
        else: 
            row["country"] = page[-3]
            row["state"] = ""
        


        # # Add address
        address = response.xpath('//div[@class="col-xs-12 pade_none muchroom_mail"]').getall()
        start=(address[0].index("/i> ")+4)
        end=address[0].index("</div>")
        address_only=address[0][start:end:]
        row["address"] = address_only

        # Add Join date
        joined = response.xpath('//div[@class="date_joined_rs"]').getall()
        start=(joined[0].index("Joined ")+7)
        end=joined[0].index("</span>")
        joined_only=joined[0][start:end:]
        row["joined"] = joined_only
   
 
        sections=response.xpath('//div[@class="col-xs-12 pad_none pricing-section-space-outer-6-11-18"]')

        prices = []
        for section in sections: 
            prices.append(self.handle_one_section(section))

        for type_of_office_prices in prices: 
            if len(type_of_office_prices["time_periods"]) != len(type_of_office_prices["prices"]): 
                errors.append(response.url)
            

            for i in range(0, len(type_of_office_prices["prices"])):
                price = type_of_office_prices["prices"][i]
                time_period = type_of_office_prices["time_periods"][i]

                unique_row = row.copy()
                unique_row["type of office"] = type_of_office_prices["type_of_price"] 
                unique_row["price"] = price
                unique_row["time period"] = time_period

                output_rows.append(unique_row)
                
        return output_rows


  
        