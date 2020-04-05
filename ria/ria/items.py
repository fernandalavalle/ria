# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


headers = ["country", "city", "state", "name", "address", "joined", "type_of_office", "price", "time_period"]


class DeskPricesRow(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    country = scrapy.Field()
    city = scrapy.Field()
    state = scrapy.Field()
    name = scrapy.Field()
    address = scrapy.Field()
    joined = scrapy.Field()
    type_of_office = scrapy.Field()
    price = scrapy.Field()
    time_period = scrapy.Field()
    
class DeskPricesError(scrapy.Item):
    url = scrapy.Field()

class DeskPricesItem(scrapy.Item):
    rows = scrapy.Field()
    errors = scrapy.Field()
    
