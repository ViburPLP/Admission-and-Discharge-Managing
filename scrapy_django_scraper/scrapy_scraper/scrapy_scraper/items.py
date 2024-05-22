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
    beneficiary_account_status = scrapy.Field()
    member_scheme = scrapy.Field()
    cover_starting = scrapy.Field()
    cover_ending = scrapy.Field()
    relationship_name = scrapy.Field()

class insurance_details(scrapy.Item):    
    cover_type = scrapy.Field()
    cover_value = scrapy.Field()
    cover_balance = scrapy.Field()