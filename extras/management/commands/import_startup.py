import csv
from django.core.management.base import BaseCommand, CommandError
from search.models import Company as Startup
from search.models import Director
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
                    gst = row['GSTIN']
                    if not gst:
                        continue
                    startup = Startup.objects.filter(gst=gst)
                    if not startup:
                        self.stdout.write(self.style.WARNING(f'Startup with GST {gst} not found'))
                        continue
                    startup = startup.first()
                    if not startup:
                        self.stdout.write(self.style.WARNING(f'Startup with GST {gst} not found'))
                        continue
                    
                    company_type = row['Company Type']
                    registration_date = row['Registration Date']
                    status = row['Status']
                    turnover = row['Aggregate Turnover']
                    aggregate_turnover_fy = row["Aggregate Turnover FY"]
                    nature_of_business = row["Nature of Business Activities"]
                    gstr_type = row["GSTR Type"]
                    ntc_reason = row["NTC Reason"]
                    members = row["Members"]
                    if company_type and not startup.company_type:
                        startup.company_type = company_type
                    if registration_date and not startup.incorporation_date:
                        startup.incorporation_date = registration_date
                    if status and not startup.status:
                        startup.status = status
                    if turnover and not startup.turnover:
                        startup.turnover = turnover
                    if aggregate_turnover_fy and not startup.aggregate_turnover_fy:
                        startup.aggregate_turnover_fy = aggregate_turnover_fy
                    if nature_of_business and not startup.nature_of_business:
                        startup.nature_of_business = nature_of_business
                    if gstr_type and not startup.gstr_type:
                        startup.gstr_type = gstr_type
                    if ntc_reason and not startup.ntc_reason:
                        startup.ntc_reason = ntc_reason
                    if members:
                        members = members.split(',')
                    for member in members:
                        if member:
                            try:
                                director = Director.objects.get(name=member, company=startup)
                            except Director.DoesNotExist:
                                director = Director(name=member, company=startup)
                                director.save()
                    startup.save()


                    self.stdout.write(self.style.SUCCESS(f'Successfully Saved {startup.name}'))

        except FileNotFoundError:
            raise CommandError(f"File '{csv_file}' does not exist.")
        except csv.Error as e:
            raise CommandError(f"Error reading CSV file: {e}")
