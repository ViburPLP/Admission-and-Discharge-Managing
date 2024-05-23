# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import mysql.connector
from scrapy.exceptions import DropItem


class ScrapyScraperPipeline:
    def process_item(self, item, spider):
        return item
    
class ScrapySaverPipeline: 
    def __init__(self):
        self.conn = mysql.connector.connect(
            host="localhost",
            user="plp",
            password="",
            database="scrapy_scraper"
        )

        self.cur = self.conn.cursor()

        ## creating table if non exists.
        self.cur.execute("""
            CREATE TABLE IF NOT EXISTS member_details (
                id INT AUTO_INCREMENT PRIMARY KEY,
                payer VARCHAR(255),
                membership_number VARCHAR(255),
                relationship VARCHAR(255),
                name VARCHAR(255),
                validity VARCHAR(255),
                status VARCHAR(255),
                scheme VARCHAR(255),
                cover_type VARCHAR(255),
                cover_value VARCHAR(255),
                cover_balance VARCHAR(255),         
                PRIMARY KEY(membership_number)
            )
        """)

        # self.cur.execute("""
        #     CREATE TABLE IF NOT EXISTS insurance_details (
        #         cover_type VARCHAR(255),
        #         cover_value VARCHAR(255),
        #         cover_balance VARCHAR(255)
        #     )
        # """)

        def process_item(self, item, spider):
            self.cur.execute(
                """INSERT INTO member_details (
                    payer, 
                    membership_number, 
                    relationship, 
                    name, 
                    validity, 
                    status, 
                    scheme) 
                    VALUES (
                        %s, %s, %s, %s, %s, %s, %s
                        )""",(
                    item['payer'],
                    item['membership_number'],
                    item['relationship'],
                    item['name'],
                    item['validity'],
                    item['status'],
                    item['scheme']
                )
            )

            member_id = self.cur.lastrowid

            for cover in item['covers']:
                self.cur.execute(
                    """INSERT INTO member_insurance_details (
                        id,
                        cover_type,
                        cover_value,
                        cover_balance) 
                        VALUES (
                            %s, %s, %s, %s
                            )""",
                    (
                        member_id,
                        cover['cover_type'],
                        cover['cover_value'],
                        cover['cover_balance']
                    )
                )

            self.conn.commit()
            return item

    def close_spider(self, spider):
        self.cur.close()
        self.conn.close()

