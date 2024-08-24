import csv
from django.core.management.base import BaseCommand, CommandError
from search.models import Company as Startup

class Command(BaseCommand):
    help = 'Imports startups data from a CSV file, skipping entries with existing names.'

    def add_arguments(self, parser):
        parser.add_argument('csv_file', type=str, help='The path to the CSV file.')

    def handle(self, *args, **kwargs):
        csv_file = kwargs['csv_file']

        # Define sector mappings
        SECTOR_MAPPING = {
            'waste_management': ['waste'],
            'supply_chain': ['supply_chain'],
            'mobility': ['mobility'],
            'agriculture': ['agriculture'],
            'health': ['health'],
            'financial_inclusion': ['financial_inclusion'],
            'other': []  # Default sector if no match is found
        }

        try:
            with open(csv_file, mode='r') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    startup_id = row['id']
                    name = row['name']
                    dipp_number = row['dippNumber']
                    dipp_recognition_status = row['dippRecognitionStatus']
                    city = row['city']
                    state = row['state']
                    industries = row.get('industries', '').strip().replace("'", '').replace('[', '').replace(']', '')
                    sectors = row.get('sectors', '').strip().replace("'", '').replace('[', '').replace(']', '')


                    if Startup.objects.filter(name=name).exists():
                        self.stdout.write(self.style.WARNING(f'Skipped {name} as it already exists.'))
                        continue

                    # Determine sector based on industries and sectors
                    sector = 'other'  # Default sector
                    for sector_key, keywords in SECTOR_MAPPING.items():
                        if any(keyword in industries.lower() or keyword in sectors.lower() for keyword in keywords):
                            sector = sector_key
                            break

                    sector = f'{industries} || {sectors}'.strip() if industries or sectors else ''
                    # breakpoint()
                    # Create the Startup instance only if it does not exist
                    Startup.objects.create(
                        startup_id=startup_id,
                        name=name,
                        dipp_number=dipp_number,
                        dipp_recognition_status=dipp_recognition_status,
                        city=city,
                        state=state,
                        sector=sector
                    )
                    self.stdout.write(self.style.SUCCESS(f'Successfully created startup {startup_id}'))

        except FileNotFoundError:
            raise CommandError(f"File '{csv_file}' does not exist.")
        except csv.Error as e:
            raise CommandError(f"Error reading CSV file: {e}")
