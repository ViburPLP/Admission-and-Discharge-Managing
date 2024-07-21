# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
# from itemadapter import ItemAdapter
# import mysql.connector
# from scrapy.exceptions import DropItem

import sys
import subprocess
import os
import time
from scrapy import signals
from scrapy.exceptions import NotConfigured



class ScrapyScraperPipeline:
    def process_item(self, item, spider):
        return item
    
# class MyPipeline:

#     @classmethod
#     def from_crawler(cls, crawler):
#         pipeline = cls()
#         crawler.signals.connect(pipeline.close_spider, signal=signals.spider_closed)
        
#         return pipeline

#     def close_spider(self, spider):
#         django_manage_py_path = 'C:/Users/Victor/Documents/Scraper/Localscraper/dash/manage.py' #path to the Django manage.py file
#         json_file_path = 'C:/Users/Victor/Documents/Scraper/Localscraper/dash/scrapy_scraper/spiders/member_details.json' #path to the scrapped JSON file
        
#         # while not os.path.exists(json_file_path) or os.path.getsize(json_file_path) == 0:
#         #     time.sleep(1) # wait for 1 second before checking again
        
#         command = f'python {django_manage_py_path} import_member {json_file_path}' #running the command file        
#         subprocess.call(command, shell=True)
    
