from datetime import datetime
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

    # @staticmethod
    # def fetch_gst_info(pan):
    #     url = 'https://pan-all-in-one.befisc.com/'
    #     data = {"pan": pan}
    #     response = APIService.fetch_json(url, data)
    #     return response['result'].get('is_director', {}).get('info', [])

    @staticmethod
    def fetch_gst_info(pan):
        url = 'https://pan-all-in-one.befisc.com/'
        data = {"pan": pan}
        response = APIService.fetch_json(url, data)
        return response['result']

    @staticmethod
    def fetch_gst_turnover(gst_no, year):
        url = 'https://gst-turnover.befisc.com'
        data = {
            "gst_no": gst_no,
            "year": year
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

    @staticmethod
    def fetch_company_name_from_gst(gst):
        url = "https://gst-verification-basic.befisc.com/"
        data = {
            "gst_number": gst
        }
        response = APIService.fetch_json(url, data)
        return response['result'].get("legal_name_of_business")

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
        director_defaults = {key: value for key, value in director_defaults.items() if value != ""}
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
    def create_gst_data(gst_data):
        try:
            gst_data_obj = GSTData.objects.get(gst_no=gst_data.get('gst_no'), year=gst_data.get('year'))
            print("GOOOOOOOOOT")
        except GSTData.DoesNotExist:
            print("CREATEEEEEEEEEE")
            gst_data_obj= GSTData.objects.create(
                    gst_no= gst_data.get('gst_no'),
                    year= gst_data.get('year'),
                    gst_estimated_total= gst_data.get('gst_estimated_total'),
                    gst_filed_total= gst_data.get('gst_filed_total'),
                    pan_estimated_total= gst_data.get('pan_estimated_total'),
                    pan_filed_total= gst_data.get('pan_filed_total'),
                    gst_status= gst_data.get('gst_status'),
                    legal_name= gst_data.get('legal_name'),
                    trade_name= gst_data.get('trade_name'),
                    register_date= gst_data.get('register_date'),
                    tax_payer_type= gst_data.get('tax_payer_type'),
                    authorized_signatory= gst_data.get('authorized_signatory'),
                    business_nature= gst_data.get('business_nature'),
                    company_name= gst_data.get('company_name'),
                
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

                        if director_obj.pan:
                            additional_info = APIService.fetch_gst_info(director_obj.pan)
                            if additional_info.get("masked_aadhaar"):
                                director_obj.masked_aadhaar = additional_info.get("masked_aadhaar")
                            if additional_info.get("phone_number"):
                                director_obj.phone_number = additional_info.get("phone_number")
                            if additional_info.get("din_info").get("company_list"):
                                director_obj.company_list = additional_info.get("din_info").get("company_list")
                            if additional_info.get("is_director").get("info"):
                                director_obj.other_director_info = additional_info.get("is_director").get("info")
                            if additional_info.get("is_sole_proprietor"):
                                director_obj.is_sole_proprietor = additional_info.get("is_sole_proprietor").get("found")
                            director_obj.save()

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


def format_academic_year(year):
    next_year = (year + 1) % 100  # Get the last two digits of the next year
    return f"{year}-{next_year:02d}"

@csrf_exempt
def fetch_gst_turnover(request):
    if request.method == 'POST':
        data = json.loads(request.body)

        company_name = data.get("company_name")
        incorporation_date = data.get("incorporation_date")
        data = data.get("data")
        output = json.loads(data.replace("'",'"'))
        
        gst_list = [item.get("gst") for item in output if item.get("gst")]
        print(gst_list)
        if gst_list:
            
            if len(gst_list) == 1:
                gst = gst_list[0]
            else:
                # Check Which GST is Of same name of company
                for gst_number in gst_list:
                    name = APIService.fetch_company_name_from_gst(gst_number)
                    if name == company_name:
                        gst = gst_number
                        break
                else:
                    return JsonResponse({'success': False})

            gst_data_objs = GSTData.objects.filter(gst_no=gst)
            if gst_data_objs:
                gst_data_list = []
                for gst_data_obj in gst_data_objs:
                    gst_data = {
                        'gst_no': gst,
                        'year': "2021-22",
                        'gst_estimated_total': gst_data_obj.gst_estimated_total,
                        'gst_filed_total': gst_data_obj.gst_filed_total,
                        'pan_estimated_total': gst_data_obj.pan_estimated_total,
                        'pan_filed_total': gst_data_obj.pan_filed_total,
                        'gst_status': gst_data_obj.gst_status,
                        'legal_name': gst_data_obj.legal_name,
                        'trade_name': gst_data_obj.trade_name,
                        'register_date': gst_data_obj.register_date,
                        'tax_payer_type': gst_data_obj.tax_payer_type,
                        'authorized_signatory': " ".join(gst_data_obj.authorized_signatory if isinstance(gst_data_obj.authorized_signatory, list) else [gst_data_obj.authorized_signatory]),
                        'business_nature': " ".join(gst_data_obj.business_nature if isinstance(gst_data_obj.business_nature, list) else [gst_data_obj.business_nature]),
                        'company_name': company_name  # make sure to define or get company_name
                    }
                    gst_data_list.append(gst_data)

                return JsonResponse({'success': True, 'gst_data': gst_data_list})
            try:
                if gst:
                    start_year = datetime.strptime(incorporation_date, "%m/%d/%Y").year
                    current_year = datetime.now().year

                    gst_data_list = []

                    for year in range(start_year, current_year):
                        formatted_year = format_academic_year(year)
                        gst_turnover_data = APIService.fetch_gst_turnover(gst, formatted_year)

                        gst_data = {
                            'gst_no': gst,
                            'year': formatted_year,
                            'gst_estimated_total': gst_turnover_data.get('gst_estimated_total'),
                            'gst_filed_total': gst_turnover_data.get('gst_filed_total'),
                            'pan_estimated_total': gst_turnover_data.get('pan_estimated_total'),
                            'pan_filed_total': gst_turnover_data.get('pan_filed_total'),
                            'gst_status': gst_turnover_data.get('gst_status'),
                            'legal_name': gst_turnover_data.get('legal_name'),
                            'trade_name': gst_turnover_data.get('trade_name'),
                            'register_date': gst_turnover_data.get('register_date'),
                            'tax_payer_type': gst_turnover_data.get('tax_payer_type'),
                            'authorized_signatory': " ".join(gst_turnover_data.get('authorized_signatory', [])),
                            'business_nature': " ".join(gst_turnover_data.get('business_nature', [])),
                            'company_name': company_name
                        }

                        GSTService.create_gst_data(gst_data)
                        gst_data_list.append(gst_data)
                    print(gst_data_list)
                    return JsonResponse({'success': True, "gst_data": gst_data_list})
                else:
                    return JsonResponse({'success': False, "message": "GST number is required."})            
            except Exception as e:
                print(f"Error fetching GST turnover: {e}")

    return JsonResponse({'success': False})

