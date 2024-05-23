# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class ScrapyScraperItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

class member_details(scrapy.Item):
    payer = scrapy.Field()
    membership_number = scrapy.Field()
    relationship = scrapy.Field()
    name = scrapy.Field()
    validity = scrapy.Field()
    status = scrapy.Field()
    scheme = scrapy.Field()


class insurance_details(scrapy.Item):    
    cover_type = scrapy.Field()
    cover_value = scrapy.Field()
    cover_balance = scrapy.Field()