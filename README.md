HTML Downloader Extension
Purpose and Functionality: this is designed to download HTML files from a specified folder for later processing by the spider. Its primary purpose is to serve as a pre-processing step, ensuring that the necessary HTML files are available for scraping. 

How It Works: The downloader is equipped with logic to fetch all .html files from a given directory, recursively searching subfolders if necessary. This is done through:

html_files = glob.glob(os.path.join(folder_path, '**/*.html'), recursive=True)

Once it locates the HTML files, it constructs the file path into a URL format compatible with Scrapy by using the file:// scheme:

file_url = f'file:///{file_path}'

This ensures that Scrapy can interpret the local files as URLs when passing them to the spider for scraping. The downloader then proceeds to yield a request to the Scrapy spider for each HTML file found:

yield Request(url=file_url, callback=self.parse_local_html, dont_filter=True)

This approach guarantees that Scrapy can process all the HTML files within the specified directory. If no HTML files are found, it logs an error:

self.logger.error('No HTML files found in the specified folder')

Error Handling: The downloader is also responsible for error handling. It handles exceptions when files cannot be read, and logs an error when a file cannot be found or read:

except FileNotFoundError:
    self.logger.error(f'File not found: {file_path}')
except Exception as e:
    self.logger.error(f'Error reading file {file_path}: {e}')

It ensures that all required HTML files are discovered and passed to the spider for further processing. It logs useful information about the files it is processing and ensures any issues with file reading or non-existent files are logged properly.

The Scrapy Spider

Purpose and Functionality: This the core data extraction tool, utilizing Scrapy to parse the locally downloaded HTML (-this directory is to be changed in deployment) files and extract specific pieces of data, including member details and insurance information. This spider is crucial for converting the raw HTML content into structured data that can later be imported into the Django database.

The spider begins its work by accepting requests for each local HTML file from the extension. Each file is then processed in the parse_local_html method:

def parse_local_html(self, response):
    self.logger.info(f'Parsing file: {response.url}')

Within this method, the spider reads the content of the HTML file and creates a TextResponse object to allow Scrapy to process the content as if it were a regular web page response. This is done by using:

local_response = TextResponse(
    url=response.url,
    body=html_content,
    encoding='UTF-8',
    request=response.request
)

This conversion ensures that Scrapy’s parsing mechanisms (e.g., CSS selectors, XPath) work seamlessly with the local files.

Data Extraction: The spider extracts specific details from the HTML files, particularly focusing on member and insurance information. For example, the member details, such as membership_number, name, and scheme, are scraped using CSS selectors:

membership_number = response.css('div.col-4 span.name::text')[3].get()
payer = response.css('div.col-4 p.body.ng-star-inserted::text').get()

Once extracted, the spider checks for the presence of the data and processes it accordingly. For instance, if the payer is found, it is cleaned and stripped of unnecessary characters like:

if payer:
    payer = payer.replace('Payer: ', '')

Similarly, the spider targets specific div elements containing insurance data, such as cover_type, cover_value, and cover_balance, by looking for certain class attributes:

insurance_divs = response.css('div.insurance.ng-star-inserted')
for div in insurance_divs:
    cover_type = div.css('p.header::text').get()
    cover_value = div.css('div > p::text').re_first(r'KSh ([\d,]+\.00)')

This data is then stored in respective insurance_details() items, which will be passed to the pipeline for further processing.

File Deletion: After processing each HTML file, the spider deletes the file to ensure that no unnecessary files are left behind. This is done through the os.remove() method:

os.remove(file_path)
self.logger.info(f'Successfully deleted file: {file_path}')

This deletion ensures that the files are managed efficiently and do not take up space unnecessarily. It also avoids reprocessing the same files during subsequent runs of the spider.

Logic for Conditional Parsing: A crucial part of the spider’s logic is determining when to parse certain data. For instance, it skips files that do not contain the keyword "Payer" in their URL:

if "Payer" not in response.url:
    self.logger.info(f'Skipping file: {response.url}')
    return

This check ensures that the spider focuses only on the relevant files, improving processing efficiency.

Item Generation: The extracted data is yielded as items for further handling in the pipeline, which would typically be the custom feed storage mechanism or other processing steps for saving the data. For example, the insurance_details() item is generated with the extracted cover type, cover value, and balance:

cover_item['cover_type'] = cover_type.strip()
cover_item['cover_value'] = cover_value.strip()
cover_item['cover_balance'] = cover_balance.strip()
yield cover_item

These items are processed and eventually saved to a JSON file for Django to handle.
How the spider and django app Interact:

Extension and Spider are tightly integrated. Extension is responsible for preparing the HTML files for processing by the extension in Spider. It ensures the HTML files are available, while spider handles parsing and extracting data from these files. Once the data is extracted and structured, it is saved in a JSON file that will be imported into the Django database.

Django Project (Dash)

Purpose and Functionality:
Dash is a Django project that serves as the backend for managing and processing the scraped data. It is primarily responsible for storing the data extracted by the Scrapy spider into a database and offering a way to manage that data through Django's ORM (Object-Relational Mapping). This app also integrates with a custom management command that processes the JSON data output by the Scrapy spider, imports it into the database, and ensures that the data is available for further use.

The key components of Dash include:

    Django Models: For storing the member and insurance data.
    Django Management Command: For importing data into the database from the JSON file generated by the spider.
    Custom Feed Storage (App 2 integration): To trigger the management command once the Scrapy spider finishes scraping and stores the data.

Models: Storing Scraped Data

In Dash, two models are defined to store the member and insurance data that the Scrapy spider (App 2) extracts. These models are:

    Member_Detail
    InsuranceDetail

Here’s a breakdown of how these models are structured:

    Member_Detail Model: This model holds the core information about each member, including their name, membership number, relationship, payer, scheme, status, and validity period.

    Example fields in the model (as inferred from the code):

class Member_Detail(models.Model):
    membership_number = models.CharField(max_length=255, unique=True)
    relationship = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    payer = models.CharField(max_length=255, null=True, blank=True)
    scheme = models.CharField(max_length=255)
    status = models.CharField(max_length=255, null=True, blank=True)
    validity = models.CharField(max_length=255, null=True, blank=True)

Each member is uniquely identified by their membership_number, and other details like relationship, name, and validity are stored as character fields.

InsuranceDetail Model: This model stores insurance-related information for each member. It includes details like cover_type, cover_value, and cover_balance, which are directly linked to the member.

Example fields:

    class InsuranceDetail(models.Model):
        cover_type = models.CharField(max_length=255)
        cover_value = models.DecimalField(max_digits=10, decimal_places=2)
        cover_balance = models.DecimalField(max_digits=10, decimal_places=2)
        member = models.ForeignKey(Member_Detail, on_delete=models.CASCADE, related_name='insurance_details')

    Here, InsuranceDetail is linked to the Member_Detail model using a foreign key relationship. This ensures that each insurance entry is tied to a specific member.

Django Management Command: Importing Scraped Data

One of the core functionalities in Dash  is the custom management command that processes the JSON file generated by the Scrapy spider. This command is responsible for importing the member and insurance data into the database.

Here’s an overview of how the management command works:

    Command Structure:
        The import_member command is designed to accept a JSON file as input, which contains the data scraped by the spider.
        The command first ensures that the provided file exists:

    if not os.path.exists(json_file):
        raise CommandError(f'File {json_file} does not exist')

Data Parsing:

    The command loads the JSON file and processes it. It separates the data into two groups: one for member details and another for insurance details:

    members_data = [entry for entry in data if 'relationship' in entry]
    insurance_data = [entry for entry in data if 'cover_type' in entry]

Importing Member Data:

    For each member entry, the command checks if the membership_number exists. If not, it creates or updates the member record in the database using Django’s update_or_create method:

member_instance, created = Member_Detail.objects.update_or_create(
    membership_number=membership_number, defaults=defaults)

If a new member is created, a success message is logged:

    self.stdout.write(self.style.SUCCESS(f'Successfully saved new member detail: {membership_number}'))

Importing Insurance Data:

    After processing the member data, the command iterates through the insurance data and links each insurance detail to the corresponding member using the membership_number:

member_instance = member_instances.get(membership_number)

The cover_value and cover_balance are converted into Decimal values before being saved:

cover_value = entry.get('cover_value').replace(',', '')
cover_balance = entry.get('cover_balance').replace(',', '')

Then the insurance details are either created or updated:

InsuranceDetail.objects.update_or_create(
    cover_type=cover_type,
    cover_value=Decimal(cover_value),
    cover_balance=Decimal(cover_balance),
    member=member_instance
)

Successful imports are logged for each insurance detail:

    self.stdout.write(self.style.SUCCESS(f'Successfully saved insurance detail: {cover_type} for member {member_instance.name}'))

File Deletion:

    Once the data has been successfully imported into the database, the command attempts to delete the JSON file to avoid redundant processing in the future:

        try:
            os.remove(json_file)
            self.stdout.write(self.style.SUCCESS(f'Successfully deleted file: {json_file}'))
        except OSError as e:
            self.stdout.write(self.style.ERROR(f'Error deleting file: {json_file}. Error: {e}'))

        This ensures that the system maintains a clean environment by removing processed files.

Integration with the spider: Custom File Feed Storage

Dash also integrates with the spider through a custom Scrapy feed storage mechanism. This integration triggers the Django management command to import the data as soon as the Scrapy spider finishes scraping and storing the data into a JSON file.

The CustomFileFeedStorage class overrides the default store method used by Scrapy to store the scraped data. Once the data is stored in the JSON file, it triggers the following method to run the import command:

def run_command(self):
    django_manage_py_path = 'C:/Users/Victor/Documents/Scraper/Localscraper/dash/manage.py'
    json_file_path = self.path
    command = f'python {django_manage_py_path} import_member {json_file_path}'
    result = subprocess.call(command, shell=True)

This subprocess call runs the import_member command, passing the path of the JSON file. The command will then process the file and import the data into the Django database. The custom feed storage ensures that the data is seamlessly integrated into the system after scraping is complete.


The end.


