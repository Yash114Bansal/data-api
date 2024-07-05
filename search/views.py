import json
import requests
from django.shortcuts import render, HttpResponse
from .models import Company, Director, GSTData
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.conf import settings
from .forms import CompanySearchForm

authkey = settings.AUTH_KEY

class APIService:
    @staticmethod
    def post_request(url, data):
        headers = {
            "Content-Type": "application/json",
            "authkey": authkey
        }
        response = requests.post(url, json=data, headers=headers)
        return response.json()

    @staticmethod
    def fetch_json(url, data):
        return APIService.post_request(url, data)

    @staticmethod
    def fetch_pan(din):
        url = 'https://kyb.befisc.com/din-to-pan'
        data = {
            "din": din,
            "consent_text": "I give my consent to DIN to PAN API to fetch my info",
            "consent": "Y"
        }
        response = APIService.fetch_json(url, data)
        return response.get('result', {}).get('pan')

    @staticmethod
    def fetch_gst_info(pan):
        url = 'https://pan-all-in-one.befisc.com/'
        data = {"pan": pan}
        response = APIService.fetch_json(url, data)
        return response['result'].get('is_director', {}).get('info', [])

    @staticmethod
    def fetch_gst_turnover(gst_no):
        url = 'https://gst-turnover.befisc.com'
        data = {
            "gst_no": gst_no,
            "year": "2021-22"
        }
        response = APIService.fetch_json(url, data)
        return response['result']

    @staticmethod
    def fetch_company_data(name):
        url = 'https://cin-lookup.befisc.com/'
        data = {"company": name}
        response = APIService.fetch_json(url, data)
        return response

    @staticmethod
    def fetch_company_details(cin):
        url = 'https://cin-number-lookup.befisc.com/'
        data = {
            "cin": cin,
            "consent": "Y",
            "consent_text": "I give my consent to cin-number-lookup api to verify cin details"
        }
        response = APIService.fetch_json(url, data)
        return response['result']

class CompanyService:
    @staticmethod
    def create_company(cin, company_info):
        company_obj, created = Company.objects.get_or_create(
            cin=cin,
            defaults={
                'name': company_info.get('companyName'),
                'incorporation_date': company_info.get('dateOfIncorporation'),
                'last_agm_date': company_info.get('lastAgmDate'),
                'registration_number': company_info.get('registrationNumber'),
                'registered_address': company_info.get('registeredAddress'),
                'balance_sheet_date': company_info.get('balanceSheetDate'),
                'category': company_info.get('category'),
                'sub_category': company_info.get('subCategory'),
                'company_class': company_info.get('class'),
                'company_type': company_info.get('companyType'),
                'paid_up_capital': company_info.get('paidUpCapital'),
                'authorised_capital': company_info.get('authorisedCapital'),
                'status': company_info.get('status'),
                'roc_office': company_info.get('rocOffice'),
                'country_of_incorporation': company_info.get('countryOfIncorporation'),
                'description_of_main_division': company_info.get('descriptionOfMainDivision'),
                'email_id': company_info.get('emailID'),
                'address_other_than_registered_office': company_info.get('addressOtherThanRegisteredOffice'),
                'number_of_members': company_info.get('numberOfMembers'),
                'active_compliance': company_info.get('activeCompliance'),
                'suspended_at_stock_exchange': company_info.get('suspendedAtStockExchange'),
                'nature_of_business': company_info.get('natureOfBusiness'),
                'status_for_efiling': company_info.get('statusForEfiling'),
                'status_under_cirp': company_info.get('statusUnderCirp'),
                'pan': company_info.get('pan'),
            }
        )
        return company_obj, created

    @staticmethod
    def get_company(cin):
        try:
            return Company.objects.get(cin=cin)
        except Company.DoesNotExist:
            return None

class DirectorService:
    @staticmethod
    def create_director(director, company_obj):
        pan = director.get('pan')
        if not pan:
            pan = APIService.fetch_pan(director.get('din'))

        director_defaults = {
            'name': director.get('name'),
            'designation': director.get('designation'),
            'date_of_appointment': director.get('dateOfAppointment'),
            'address': director.get('address'),
            'pan': pan,
            'no_of_companies': director.get('noOfCompanies', 0),
            'father_name': director.get('fatherName'),
            'dob': director.get('dob'),
            'split_address': " ".join(director.get('splitAddress', []))
        }
        try:
            director_obj, created = Director.objects.update_or_create(
                din=director['din'],
                company=company_obj,
                defaults=director_defaults
            )
            return director_obj
        except Exception as e:
            print(f"Error saving director {director.get('name')}: {e}")
            return None

    @staticmethod
    def get_director(pan):
        try:
            return Director.objects.get(pan=pan)
        except Director.DoesNotExist:
            return None

class GSTService:
    @staticmethod
    def create_gst_data(director_obj, gst_data):
        try:
            gst_data_obj = GSTData.objects.get(gst_no=gst_data.get('gst_no'))
        except GSTData.DoesNotExist:
            gst_data_obj, created = GSTData.objects.get_or_create(
                director=director_obj,
                defaults={
                    'gst_no': gst_data.get('gst_no'),
                    'year': gst_data.get('year'),
                    'gst_estimated_total': gst_data.get('gst_estimated_total'),
                    'gst_filed_total': gst_data.get('gst_filed_total'),
                    'pan_estimated_total': gst_data.get('pan_estimated_total'),
                    'pan_filed_total': gst_data.get('pan_filed_total'),
                    'gst_status': gst_data.get('gst_status'),
                    'legal_name': gst_data.get('legal_name'),
                    'trade_name': gst_data.get('trade_name'),
                    'register_date': gst_data.get('register_date'),
                    'tax_payer_type': gst_data.get('tax_payer_type'),
                    'authorized_signatory': gst_data.get('authorized_signatory'),
                    'business_nature': gst_data.get('business_nature'),
                }
            )
        return gst_data_obj

def search_company(request):
    if request.method == 'POST':
        company_name = request.POST.get('company_name')
        if company_name:
            company_data = APIService.fetch_company_data(company_name)
            result = company_data.get('result')
            if company_data["status"] == 2:
                return HttpResponse("<h1>No result found</h1>")

            if result is None:
                return HttpResponse("<h1>No result found</h1>")

            cin = result[0]['cin']
            company_obj = CompanyService.get_company(cin)

            if not company_obj:
                company_details = APIService.fetch_company_details(cin)
                company_info = company_details
                director_details = company_info.get('directorDetails', [])

                # Save or update company details
                company_obj, created = CompanyService.create_company(cin, company_info)

                director_data_objects = []
                for director in director_details:
                    director_obj = DirectorService.create_director(director, company_obj)
                    if director_obj and director_obj not in director_data_objects:
                        director_data_objects.append(director_obj)

                context = {
                    'company_obj': company_obj,
                    'director_data_objects': director_data_objects,
                }
                return render(request, 'company_results.html', context)
            else:
                directors = Director.objects.filter(company=company_obj)
                context = {
                    'company_obj': company_obj,
                    'director_data_objects': directors,
                }
                return render(request, 'company_results.html', context)
    form = CompanySearchForm()
    return render(request, 'company_search.html', {'form': form})

@csrf_exempt
def fetch_gst_turnover(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        pan = data.get('pan')

        if pan:
            director_obj = DirectorService.get_director(pan)
            if director_obj:
                gst_data_obj = GSTData.objects.filter(director=director_obj).first()
                if gst_data_obj:
                    return JsonResponse({'success': True, "gst_data": gst_data_obj})

                try:
                    gst_data_list = APIService.fetch_gst_info(pan)
                    if gst_data_list:
                        gst_no = gst_data_list[0].get('gst')
                        if gst_no:
                            gst_turnover_data = APIService.fetch_gst_turnover(gst_no)

                            gst_data = {
                                'gst_no': gst_no,
                                'year': "2021-22",
                                'gst_estimated_total': gst_turnover_data.get('gst_estimated_total'),
                                'gst_filed_total': gst_turnover_data.get('gst_filed_total'),
                                'pan_estimated_total': gst_turnover_data.get('pan_estimated_total'),
                                'pan_filed_total': gst_turnover_data.get('pan_filed_total'),
                                'gst_status': gst_turnover_data.get('gst_status'),
                                'legal_name': gst_turnover_data.get('legal_name'),
                                'trade_name': gst_turnover_data.get('trade_name'),
                                'register_date': gst_turnover_data.get('register_date'),
                                'tax_payer_type': gst_turnover_data.get('tax_payer_type'),
                                'authorized_signatory': " ".join(gst_turnover_data.get('authorized_signatory')),
                                'business_nature': " ".join(gst_turnover_data.get('business_nature')),
                            }
                            GSTService.create_gst_data(director_obj, gst_data)
                            return JsonResponse({'success': True, "gst_data": gst_data})
                except Exception as e:
                    print(f"Error fetching GST turnover: {e}")

        return JsonResponse({'success': False})
    return JsonResponse({'success': False})
