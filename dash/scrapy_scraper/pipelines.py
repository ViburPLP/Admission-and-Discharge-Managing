# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
# from itemadapter import ItemAdapter
# import mysql.connector
# from scrapy.exceptions import DropItem

import os
import django
import sys
import logging
from asgiref.sync import sync_to_async
from django.db import transaction


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dash.settings')
django.setup()
sys.path.append(os.path.dirname(os.path.abspath('.'))) 
django.setup()

from dashed.models import Member_Detail, InsuranceDetail



class ScrapyScraperPipeline:
    async def process_item(self, item, spider):
        await sync_to_async(self.save_items)(item)
        return item

    @transaction.atomic
    def save_items(self, item):
        logger = logging.getLogger('django')
        logger.info(f"saving member detail for: {item['name']}")

        member_detail = Member_Detail.objects.create(
            relationship=item['relationship'],
            name=item['name'],
            membership_number=item['membership_number'],
            payer=item['payer'],
            scheme=item['scheme'],
            status=item['status'],
            validity=item['validity']
        )

        for insurance_item in item['insurance_details']:            
            if 'cover_type' in item:
                cover_type = item.get('cover_type')
                cover_value = item.get('cover_value').replace(',', '')
                cover_balance = item.get('cover_balance').replace(',', '')

                InsuranceDetail.objects.create(
                    cover_type=cover_type,
                    cover_value=float(cover_value) if cover_value else 0.0,
                    cover_balance=float(cover_balance) if cover_balance else 0.0,
                )
                self.stdout.write(self.style.SUCCESS(f'Successfully saved insurance detail: {cover_type}'))

            # logger.info(f"saving insurance detail for: {item['name']}: {insurance_item['cover_type']}: {insurance_item['cover_value']}: {insurance_item['cover_balance']}")
            # InsuranceDetail.objects.create(
            #     member=member_detail,
            #     cover_type=insurance_item['cover_type'],
            #     cover_value=insurance_item['cover_value'],
            #     cover_balance=insurance_item['cover_balance']
            # )


# class ScrapyScraperPipeline:

#     @sync_to_async
#     def save_member_detail(self, item):
#         member_detail = Member_Detail(
#             relationship=item['relationship'],
#             name=item['name'],
#             membership_number=item['membership_number'],
#             payer=item['payer'],
#             scheme=item['scheme'],
#             status=item['status'],
#             validity=item['validity']
#         )
#         member_detail.save()

#     async def process_item(self, item, spider):
#         await self.save_member_detail(item)
#         return item
    
#     @sync_to_async
#     def save_insurance_detail(self, item):
#         insurance_detail = InsuranceDetail(
#             cover_type=item['cover_type'],
#             cover_value=item['cover_value'],
#             cover_balance=item['cover_balance']
#         )
#         insurance_detail.save()

#     async def process_item(self, item, spider):
#         await self.save_insurance_detail(item)
#         return item


class ScrapyScraperPipeline:
    def process_item(self, item, spider):
        return item
    
# class ScrapySaverPipeline: 
#     def __init__(self):
#         self.conn = mysql.connector.connect(
#             host="localhost",
#             user="plp",
#             password="",
#             database="scrapy_scraper"
#         )

#         self.cur = self.conn.cursor()

#         ## creating table if non exists.
#         self.cur.execute("""
#             CREATE TABLE IF NOT EXISTS member_details (
#                 payer VARCHAR(255),
#                 membership_number VARCHAR(255),
#                 relationship VARCHAR(255),
#                 name VARCHAR(255),
#                 validity VARCHAR(255),
#                 status VARCHAR(255),
#                 scheme VARCHAR(255),
#                 cover_type VARCHAR(255),
#                 cover_value VARCHAR(255),
#                 cover_balance VARCHAR(255),         
#                 PRIMARY KEY(membership_number)
#             )
#         """)

#         self.cur.execute("""
#             CREATE TABLE IF NOT EXISTS insurance_details (
#                 cover_type VARCHAR(255),
#                 cover_value VARCHAR(255),
#                 cover_balance VARCHAR(255),
#                 FOREIGN KEY (membership_number) REFERENCES member_details(membership_number)
#             )
#         """)

#     def process_item(self, item, spider):
#         self.cur.execute(
#             """INSERT INTO member_details (
#                 payer, 
#                 membership_number, 
#                 relationship, 
#                 name, 
#                 validity, 
#                 status, 
#                 scheme) 
#                 VALUES (
#                     %s, %s, %s, %s, %s, %s, %s
#                     )""",(
#                 item['payer'],
#                 item['membership_number'],
#                 item['relationship'],
#                 item['name'],
#                 item['validity'],
#                 item['status'],
#                 item['scheme']
#             )
#         )

#         self.conn.commit()
#         return item

#     def close_spider(self, spider):
#         self.cur.close()
#         self.conn.close()



