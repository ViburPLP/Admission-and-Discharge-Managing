import os
import subprocess
from scrapy.extensions.feedexport import FileFeedStorage

class CustomFileFeedStorage(FileFeedStorage):

    def __init__(self, uri, *args, **kwargs):
        super().__init__(uri, *args, **kwargs)
        self.uri = uri
        self.path = self._get_path(uri)

    def store(self, file):
        super().store(file)
        print(f"Storing file at: {self.path}")  # Debugging statement
        self.run_command()

    def run_command(self):
        django_manage_py_path = 'C:/Users/Victor/Documents/Scraper/Localscraper/dash/manage.py'
        json_file_path = self.path
        print(f"Running command: python {django_manage_py_path} import_member {json_file_path}")  # Debugging statement
        command = f'python {django_manage_py_path} import_member {json_file_path}'
        result = subprocess.call(command, shell=True)
        print(f"Command executed with result: {result}")  # Debugging statement

    def _get_path(self, uri):
        if uri.startswith('file://'):
            path = uri[7:] if os.name != 'nt' else uri[8:].replace('/', '\\')
        else:
            path = uri
        return path
