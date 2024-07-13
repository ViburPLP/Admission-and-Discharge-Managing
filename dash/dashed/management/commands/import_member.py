import json
import os
import sys
from decimal import Decimal
from django.core.management.base import BaseCommand, CommandError
from dashed.models import Member_Detail, InsuranceDetail

sys.path.append(os.path.dirname(os.path.abspath('.')))

class Command(BaseCommand):
    help = 'Import member details from json file'

    def add_arguments(self, parser):
        parser.add_argument('json_file', type=str) 

    def handle(self, *args, **kwargs):
        json_file = kwargs['json_file']

        if not os.path.exists(json_file):
            raise CommandError(f'File {json_file} does not exist')

        with open(json_file, 'r') as file:
            data = json.load(file)

        members_data = [entry for entry in data if 'relationship' in entry]
        insurance_data = [entry for entry in data if 'cover_type' in entry]

        member_instances = {}
        for entry in members_data:
            if 'relationship' in entry:
                membership_number = entry.get('membership_number')
                defaults = {
                    'relationship': entry.get('relationship'),
                    'name': entry.get('name'),
                    'payer': entry.get('payer'),
                    'scheme': entry.get('scheme'),
                    'status': entry.get('status'),
                    'validity': entry.get('validity')
                }

                member_instance, created = Member_Detail.objects.update_or_create(
                    membership_number=membership_number, defaults=defaults)

                member_instances[membership_number] = member_instance
                if created:
                    self.stdout.write(self.style.SUCCESS(f'Successfully saved new member detail: {membership_number}'))
                else:
                    self.stdout.write(self.style.SUCCESS(f'Successfully updated member detail: {membership_number}'))


        for entry in insurance_data:
            cover_type = entry.get('cover_type')
            cover_value = entry.get('cover_value').replace(',', '')
            cover_balance = entry.get('cover_balance').replace(',', '')

            member_instance = member_instances.get(membership_number)
            
            if member_instance:
                InsuranceDetail.objects.update_or_create(
                    cover_type=cover_type,
                    cover_value=Decimal(cover_value) if cover_value else Decimal('0.0'),
                    cover_balance=Decimal(cover_balance) if cover_balance else Decimal('0.0'),
                    member=member_instance
                )
                self.stdout.write(self.style.SUCCESS(f'Successfully saved insurance detail: {cover_type} for member {member_instance.name}'))
            else:
                self.stdout.write(self.style.ERROR(f'No member instance found for insurance detail: {entry}'))

        self.stdout.write(self.style.SUCCESS('Successfully imported all data'))


      
        self.stdout.write(self.style.SUCCESS('Successfully imported all data'))

        # The handle method processes the JSON file in two separate loops:
        # 1. The first loop processes member details.
        # 2. The second loop processes insurance details.
         
        # This separation ensures that member instances are created first,
        # so that when the insurance details are processed, they can be correctly
        # associated with existing member instances.
         
        # If both member and insurance details were processed within a single loop,
        # insurance details would be created without an associated member instance,
        # resulting in a blank insurancedetails table.
        # believe you me, this was hectic. 

