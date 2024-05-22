import os
import glob
import scrapy
from scrapy.http import Request, TextResponse
from urllib.parse import urljoin

class MemberScrapSpider(scrapy.Spider):
        name = 'memberScrap'


        def start_requests(self):
            folder_path = "C:/Users/Victor/Downloads/"
            html_files = glob.glob(os.path.join(folder_path, '*.html'))

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
            print(response.body.decode('utf-8'))

    # def start_requests(self):
    #     folder_path = "C:/Users/Victor/Downloads/"
    #     # html_files = 
    #    Print (glob.glob(os.path.join(folder_path, '*.html')))

    #     if not html_files:
    #         self.logger.error('No HTML files found in the specified folder')
    #         return

    #     for html_file in html_files:
    #         file_url = urljoin('file:', os.path.abspath(html_file))
    #         yield Request(url=file_url, callback=self.parse_local_html, dont_filter=True)

    # def parse_local_html(self, response):
    #     file_path = response.url.replace('file:///', '', 1)
    #     with open(file_path, 'r', encoding='UTF-8') as f:
    #         html_content = f.read()

    #     local_response = TextResponse(
    #         url=response.url,
    #         body=html_content,
    #         encoding='UTF-8',
    #         request=response.request
    #     )

    #     self.parse(local_response)

    # def parse(self, response):
    #     print(response.body.decode('utf-8'))

    #     account_details = response.css('div.col-4 p.header::text').get()
    #     payer = response.css('div.col-4 p.body.ng-star-inserted::text').get()
    #     membership_number = response.css('div.col-4 span.name::text')[3].get()
    #     beneficiary_account_status = response.css('div.col-4 span.name::text')[4].get()
    #     member_scheme = response.css('div.col-4 span.name::text').getall()[-1]
    #     headers = response.css('div.insurance p.header::text').getall()
    #     covers = response.css('div.insurance p::text').getall()
    #     balances = response.css('div.insurance p.label span + ::text').getall()

    #     for i in range(len(headers)):
    #         if headers[i] == 'OUT-PATIENT':
    #             cover = covers[i]
    #             balance = balances[i]
    #             print('Cover:', cover)
    #             print('Balance:', balance)
    #             break





    #     member_info = response.css #(I will add the specific part to scrape)

    #     member_name = member_info.css #specific location.('p::text').extract_first()

        # start_urls = ['file:///C:/Users/Victor/Desktop/Payer%20Portal_files/Payer%20Portal.html']

       



    #     # yield ScrapedDataItem()
