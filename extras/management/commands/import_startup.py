import csv
from django.core.management.base import BaseCommand, CommandError
from search.models import Company as Startup

class Command(BaseCommand):
    help = 'Imports startups data from a CSV file, skipping entries with existing names.'

    def add_arguments(self, parser):
        parser.add_argument('csv_file', type=str, help='The path to the CSV file.')

    def handle(self, *args, **kwargs):
        csv_file = kwargs['csv_file']
        

        try:
            with open(csv_file, mode='r') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    pan = row['pan']
                    gst = row['gstin']
                    if not pan or not gst:
                        continue
                    if gst == "No GSTIN found":
                        continue
                    startup = Startup.objects.filter(pan=pan)
                    if not startup:
                        self.stdout.write(self.style.WARNING(f'Startup with PAN {pan} not found'))
                        continue
                    startup = startup.first()
                    if not startup:
                        self.stdout.write(self.style.WARNING(f'Startup with PAN {pan} not found'))
                        continue

                    startup.gst = gst
                    startup.save()

                    self.stdout.write(self.style.SUCCESS(f'Successfully Saved startup with PAN {pan}'))

        except FileNotFoundError:
            raise CommandError(f"File '{csv_file}' does not exist.")
        except csv.Error as e:
            raise CommandError(f"Error reading CSV file: {e}")
