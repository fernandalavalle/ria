import csv
# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


class RiaPipeline(object):
    HEADERS = ["country", "city", "state", "name", "address", "joined", "type_of_office", "price", "time_period"]
    HEADERS_ERROR = ["url"]
    OUTPUT_FILE = "ria.csv"
    ERROR_FILE = "ria_errors.csv"

    def open_spider(self, spider):
        self.output_file = open(RiaPipeline.OUTPUT_FILE, 'w')
        self.error_file = open(RiaPipeline.ERROR_FILE, 'w')

        self.writer = csv.DictWriter(self.output_file, fieldnames=RiaPipeline.HEADERS)
        self.error_writer = csv.writer(self.error_file)

        self.writer.writeheader()

    def close_spider(self, spider):
        self.output_file.close()
        self.error_file.close()

    def process_item(self, item, spider):
        rows = item["rows"]
        errors = item["errors"]

        print("I'M IN THE PIPELINES")

        for row in rows: 
            self.writer.writerow(row)

        for error in errors: 
            self.error_writer.writerow(error)
