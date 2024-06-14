import json
from django.core.management.base import BaseCommand
from admissions.models import MemberDetail

class Command(BaseCommand):
    help = 'Import member details from a JSON file'

    def add_arguments(self, parser):
        parser.add_argument('json_file', type=str, help='The JSON file to import')

    def handle(self, *args, **kwargs):
        json_file = kwargs['json_file']

        with open(json_file, 'r') as file:
            data = json.load(file)
            for item in data:
                MemberDetail.objects.create(
                    payer=item.get('payer'),
                    membership_number=item.get('membership_number'),
                    relationship=item.get('relationship'),
                    name=item.get('name'),
                    validity=item.get('validity'),
                    status=item.get('status'),
                    scheme=item.get('scheme')
                )
        self.stdout.write(self.style.SUCCESS('Successfully imported data from %s' % json_file))
