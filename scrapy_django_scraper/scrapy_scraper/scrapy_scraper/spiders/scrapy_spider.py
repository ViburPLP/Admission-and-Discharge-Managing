import os
import glob
import scrapy
from scrapy.http import Request, TextResponse
from urllib.parse import unquote
from scrapy_scraper.items import member_details, insurance_details

class MemberScrapSpider(scrapy.Spider):
        name = 'memberScrap'


        def start_requests(self):
            folder_path = "C:/Users/Victor/Downloads/"
            html_files = glob.glob(os.path.join(folder_path, '**/*.html'), recursive=True)

            if not html_files:
                self.logger.error('No HTML files found in the specified folder')
                return
            
            for html_file in html_files:
                file_path = os.path.abspath(html_file).replace("\\", "/")
                file_url = f'file:///{file_path}'
                # file_url = f'file:///{os.path.abspath(html_file).replace("\\", "/")}'
                self.logger.info(f'Processing file: {file_url}')
                yield Request(url=file_url, callback=self.parse_local_html, dont_filter=True)

        
        def parse_local_html(self, response):
            self.logger.info(f'Parsing file: {response.url}')
            file_path = unquote(response.url.replace('file:///', '', 1))
            try:
                with open(file_path, 'r', encoding='UTF-8') as f:
                    html_content = f.read()
                self.logger.info(f'Successfully read file: {file_path}')
            except FileNotFoundError:
                self.logger.error(f'File not found: {file_path}')
                return
            except Exception as e:
                self.logger.error(f'Error reading file {file_path}: {e}')
                return

            local_response = TextResponse(
                url=response.url,
                body=html_content,
                encoding='UTF-8',
                request=response.request
            )

            # Directly call the parse method
            return self.parse(local_response)

        def parse(self, response):
            if "Payer" not in response.url:
                self.logger.info(f'Skipping file: {response.url}')
                return

            self.logger.info(f'Parsing content from: {response.url}')

            insurance_divs= response.css('div.insurance.ng-star-inserted')

            for div in insurance_divs: 
                cover_type = div.css('p.header::text').get()
                cover_value = div.css('div > p::text').re_first(r'Cover: (.+)')
                cover_balance = div.css('p.label::text').get()

                cover_item = insurance_details()
                cover_item['cover_type'] = cover_type
                cover_item['cover_value'] = cover_value
                cover_item['cover_balance'] = cover_balance
                
                yield cover_item

                # print ('\n'* 2 + cover_type, 
                #        '\n'* 1 + cover_value, 
                #        '\n'* 1 + cover_balance)

            item = member_details()
            
            item['payer'] = response.css('div.col-4 p.body.ng-star-inserted::text').get()
            item['membership_number'] = response.css('div.col-4 span.name::text')[3].get()
            item['beneficiary_account_status'] = response.css('div.col-4 span.name::text')[4].get()
            item['member_scheme'] = response.css('p.body:nth-child(1)::text').get()
            item['cover_starting'] = response.css('div.col-4:nth-child(1) > div:nth-child(9) > p:nth-child(2)::text').get()
            item['cover_ending'] = response.css('div.col-4:nth-child(1) > div:nth-child(9) > p:nth-child(3)::text').get()
            item['relationship_name'] = response.css('.cp-breadcrumb__current::text').get()
            relationship_name = response.css('.cp-breadcrumb__current::text').get()
            if relationship_name:
             relationship, name = map(str.strip, relationship_name.split(' - '))    
            else:
                relationship = name = None

            print (relationship, 
                   '\n' * 1 + name)
            print ('******')
          
            yield item

            # payer = response.css('div.col-4 p.body.ng-star-inserted::text').get()
            # membership_number = response.css('div.col-4 span.name::text')[3].get()
            # beneficiary_account_status = response.css('div.col-4 span.name::text')[4].get()
            # member_scheme = response.css('p.body:nth-child(1)::text').get()
            # cover_starting = response.css('div.col-4:nth-child(1) > div:nth-child(9) > p:nth-child(2)::text').get()
            # cover_ending = response.css('div.col-4:nth-child(1) > div:nth-child(9) > p:nth-child(3)::text').get()
            # relationship_name = response.css('.cp-breadcrumb__current::text').get()

            # print('\n' * 2 + 'Payer:', payer, 
            #       '\n' * 2 + 'Membership Number:', membership_number, 
            #       '\n' * 2 + 'Beneficiary Account Status:', beneficiary_account_status, 
            #       '\n' * 2 + 'Member Scheme:', member_scheme,
            #       '\n' * 2 + 'Cover Starting:', cover_starting,
            #       '\n' * 2 + 'Cover Ending:', cover_ending,
            #       '\n' * 2 + 'Relationship Name:', relationship_name 
            # )
            
            


            