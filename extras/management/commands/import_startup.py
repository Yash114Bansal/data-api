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
                    startup_id = row['user.uniqueId']
                    cin = row.get('user.startup.cin', '').strip()
                    try:
                        number = float(cin)
                        formatted_number = "{:.0f}".format(number)
                        cin = str(formatted_number)
                    except:
                        pass
                    try:
                        startup = Startup.objects.get(startup_id=startup_id)
                    except Startup.DoesNotExist:
                        startup = Startup.objects.get(cin=cin)
                    except Startup.DoesNotExist:
                        self.stdout.write(self.style.WARNING(f'Startup {startup_id} does not exist. Skipping.'))
                        continue
                    email = row.get('user.email', '').strip()
                    pan = row.get('user.startup.pan', '').strip()
                    stage = row.get('user.startup.stage', '').strip()
                    website = row.get('user.startup.website', '').strip()
                    mobile_app_link = row.get('user.startup.mobileAppLink', '').strip()
                    industries_id = row.get('user.startup.focusArea.industry.id', '').strip()
                    industries_name = row.get('user.startup.focusArea.industry.name', '').strip()
                    industries_industryName = row.get('user.startup.focusArea.industry.industryName', '').strip()
                    sectors_id = row.get('user.startup.focusArea.sectors.0.id', '').strip()
                    sectors_name = row.get('user.startup.focusArea.sectors.0.name', '').strip()
                    sectors_sectionName = row.get('user.startup.focusArea.sectors.0.sectionName', '').strip()
                    # Legal
                    dipp_certified = row.get('user.startup.dippCertified', '').strip()
                    dipp_number = row.get('user.startup.dippNumber', '').strip()
                    dipp_recognition_status = row.get('user.startup.dippRecognitionStatus', '').strip()
                    form56_applied = row.get('user.startup.form56Applied', '').strip()
                    form56_status = row.get('user.startup.form56Status', '').strip()
                    form80iac_applied = row.get('user.startup.form80IacApplied', '').strip()
                    form80iac_status = row.get('user.startup.form80IacStatus', '').strip()

                    # Funding and Connectivity:
                    funded = row.get('user.startup.funded', '').strip()
                    looking_to_connect_to = [
                        row.get(f'user.startup.lookingToConnectTo.{i}', '').strip()
                        for i in range(5)
                    ]

                    location_country = row.get('user.startup.location.country.name', '').strip()
                    location_state = row.get('user.startup.location.state.name', '').strip()
                    location_city = row.get('user.startup.location.city.name', '').strip()
                    location_district = row.get('user.startup.location.city.districtName', '').strip()
                    recognition_form_request_id = row.get('user.startup.recognitionFormRequest.id', '').strip()
                    due_diligence_request_id = row.get('user.startup.dueDiligence.requestId', '').strip()
                    incubation_program_request_id = row.get('user.startup.incubationProgram.requestId', '').strip()

                    updates = {
                        'email_id': email,
                        'cin': cin,
                        'pan': pan,
                        'stage': stage,
                        'website': website,
                        'mobile_app_link': mobile_app_link,
                        'industries_id': industries_id,
                        'industries_name': industries_name,
                        'industries_industryName': industries_industryName,
                        'sectors_id': sectors_id,
                        'sectors_name': sectors_name,
                        'sectors_sectionName': sectors_sectionName,
                        'dipp_certified': dipp_certified,
                        'dipp_number': dipp_number,
                        'dipp_recognition_status': dipp_recognition_status,
                        'form56_applied': form56_applied,
                        'form56_status': form56_status,
                        'form80iac_applied': form80iac_applied,
                        'form80iac_status': form80iac_status,
                        'funded': funded,
                        'looking_to_connect_to': looking_to_connect_to,
                        'location_country': location_country,
                        'location_state': location_state,
                        'location_city': location_city,
                        'location_district': location_district,
                        'recognition_form_request_id': recognition_form_request_id,
                        'due_diligence_request_id': due_diligence_request_id,
                        'incubation_program_request_id': incubation_program_request_id,
                    }
                    try:
                        for field, value in updates.items():
                            if value and not getattr(startup, field):  # Only update if the value is not empty
                                setattr(startup, field, value)
                        startup.save()
                    except Exception as e:
                        self.stdout.write(self.style.ERROR(f'Failed to save startup {startup_id} name {startup.name}'))
                        self.stdout.write(self.style.ERROR(f'Error: {e}'))
                        continue
                    self.stdout.write(self.style.SUCCESS(f'Successfully Saved startup {startup_id} name {startup.name}'))

        except FileNotFoundError:
            raise CommandError(f"File '{csv_file}' does not exist.")
        except csv.Error as e:
            raise CommandError(f"Error reading CSV file: {e}")
