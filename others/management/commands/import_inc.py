import os
import pandas as pd
from django.core.management.base import BaseCommand
from others.models import Incubator

class Command(BaseCommand):
    help = 'Import Incubators data from an Excel file'

    def add_arguments(self, parser):
        parser.add_argument('file_path', type=str, help='The path to the Excel file to be imported')

    def handle(self, *args, **kwargs):
        file_path = kwargs['file_path']
        if not os.path.exists(file_path):
            self.stdout.write(self.style.ERROR(f"File {file_path} does not exist"))
            return

        # Load the Excel file
        df = pd.read_excel(file_path)

        for _, row in df.iterrows():
            a = Incubator.objects.create(
                unique_id=row['Unique ID'],
                email=row['Email'],
                phone=row['Phone'],
                pan=row['PAN'],
                role=row['Role'],
                company_name=row['Company Name'],
                incubation_centers_locations=row['Incubator Center Locations'],
                country=row['Country'],
                state=row['State'],
                city=row['City'],
                description=row['Description'],
                industry=row['Industry'],
                sectors=row['Sectors'],
                first_name=row['First Name'],
                last_name=row['Last Name'],
                designation=row['Designation'],
                email_id=row['Email ID'],
                mobile_number=row['Mobile Number'],
                landline_number=row['Landline Number'],
                website=row['Website'],
                social_media_url=row['Social Media URL'],
            )
            # breakpoint()

        self.stdout.write(self.style.SUCCESS(f"Successfully imported data from {file_path}"))
