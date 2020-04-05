import scrapy
import json
import re
import requests

from scrapy.linkextractors import LinkExtractor

from ria import items

ERROR_FILE = "errors.txt"

headers = ["country", "city", "state", "name", "address", "joined", "type_of_office", "price", "time_period"]

class DeskPriceSpider(scrapy.Spider):
    name = "desk_price"

    allowed_domains = ['coworker.com']
    countries = [("Brazil", "31"),("United+states", "231")]
    request_headers = {
        "x-requested-with" : "XMLHttpRequest", 
        "content-type" : "application/x-www-form-urlencoded; charset=UTF-8", 
    }
    request_body = "ci_csrf_token=&pIdx={}&placeId={}&lvl=1&sfilter=all&splan=open&sammenities=&saccs=0&sapps=0&sdeposit=0&scapacity=0&scrypto=0&search={}&x_1=&x_2=&y_1=&y_2="

    def start_requests(self):
        request_batch = []
        for country in DeskPriceSpider.countries: 
            more_pages = True
            pIdx = 0
            while more_pages: 
                response = requests.post("https://www.coworker.com/search/get_pagination", 
                                            data=DeskPriceSpider.request_body.format(pIdx, country[1], country[0]), 
                                            headers=DeskPriceSpider.request_headers)


                for specific_place in response.json()["content"]: 
                    relative_url = specific_place["s_url"]
                    request_batch.append(scrapy.Request(url="https://www.coworker.com/" + relative_url, callback=self.parse_specific_page_response))

                ((left, right), last_result) = self.parse_pagination(response.json()["sh"])
                current_number_of_results = len(response.json()["content"])
                pIdx+=1

                if (int(right) + int(current_number_of_results) >= int(last_result)): 
                    more_pages = False

        print("length of requests")
        print(len(request_batch))
        return request_batch

    def parse_pagination(self, pagination_string):
        result_range = re.search(r"([-+]?\d+)-([-+]?\d+)", pagination_string).groups()
        result_max = re.search(r"of ([-+]?\d+)", pagination_string).group(0).strip("of").strip()
        return (result_range, result_max)


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
   

    def parse_specific_page_response(self, response):
        output_rows = []
        errors = []

        row = {}
        page = response.url.split("/")
        
        row["name"] = page[-1]
        row["city"] = page[-2]

        if ("united-states" in page): 
            row["country"] = page[-4]
            row["state"] = page[-3]
        else: 
            row["country"] = page[-3]
            row["state"] = ""
        
        try: 

            #  # Add address
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

        except IndexError:
            pass
 
        sections=response.xpath('//div[@class="col-xs-12 pad_none pricing-section-space-outer-6-11-18"]')

        prices = []
        for section in sections: 
            prices.append(self.handle_one_section(section))

        for type_of_office_prices in prices: 
            if len(type_of_office_prices["time_periods"]) != len(type_of_office_prices["prices"]): 
                errors.append(items.DeskPricesError(url=response.url))
            

            for i in range(0, len(type_of_office_prices["prices"])):
                price = type_of_office_prices["prices"][i]
                time_period = type_of_office_prices["time_periods"][i]

                unique_row = row.copy()
                unique_row["type_of_office"] = type_of_office_prices["type_of_price"] 
                unique_row["price"] = price
                unique_row["time_period"] = time_period

                output_rows.append(items.DeskPricesRow(unique_row))
                
        return items.DeskPricesItem(rows=output_rows, errors=errors)


  
        