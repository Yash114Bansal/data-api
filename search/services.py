import datetime
import os
import re
import gspread
from typing import List
from django.conf import settings


def initialize_gspread() -> gspread.client.Client:
    """
    Initialize a gspread client with the given credentials.
    """
    return gspread.service_account_from_dict(
        get_credentials()
    )


def get_credentials() -> dict:
    """
    Return gspread credentials.
    """
    return {
        "type": os.getenv("TYPE"),
        "project_id": os.getenv("PROJECT_ID"),
        "private_key_id": os.getenv("PRIVATE_KEY_ID"),
        "private_key": os.getenv("PRIVATE_KEY"),
        "client_email": os.getenv("CLIENT_EMAIL"),
        "client_id": os.getenv("CLIENT_ID"),
        "auth_uri": os.getenv("AUTH_URI"),
        "token_uri": os.getenv("TOKEN_URI"),
        "auth_provider_x509_cert_url": os.getenv("AUTH_PROVIDER_X509_CERT_URL"),
        "client_x509_cert_url": os.getenv("CLIENT_X509_CERT_URL"),
        "universe_domain": os.getenv("UNIVERSE_DOMAIN"),
    }


def get_all_rows(doc_name: str) -> List[dict]:
    """
    Fetches all rows from a given Google Sheet worksheet.
    """
    sh = settings.GSPREAD_CLIENT.open(doc_name)
    worksheet =  sh.get_worksheet(0)
    return worksheet.get_all_records()




def is_sheet_updated(doc_name: str) -> bool:
    client = settings.GSPREAD_CLIENT
    sh = client.open(doc_name)
    props = sh.fetch_sheet_metadata()  # Example function to fetch metadata
    # print(props)
    modifiedTime = client.get_file_drive_metadata(props["spreadsheetId"]).get("modifiedTime")
    sheet_last_modified = datetime.datetime.strptime(modifiedTime, '%Y-%m-%dT%H:%M:%S.%fZ')
    return sheet_last_modified > datetime.datetime.now() - datetime.timedelta(hours=6)

def get_value_or_none(row, field):
    value = row.get(field)
    return value if value else None

def getFormattedRow(row, sheetName):
    if "WhatsApp Bot" in sheetName:
        return {
            **row,
            "source": "Whatsapp Bot"
            }
    if 'Google Drive' in sheetName:
        formattedRow = {
            "Company": row.get("Name of the Company"),
            "Mobile Number": row.get("Mobile Number"),
            "Founder": row.get("What is your name?"),
            "About": row.get("What does your company do?"),
            "Current Status": row.get("Current Status"),
            "Sector": row.get("Sector"),
            "SubSector": row.get('Mention if it\'s "Other"'),
            "Email": row.get("Enter your Email"),
            "12MRevenue": row.get('Revenue in the last 1 year? (In Rupees) \nEg. 40,00,000'),
            "Equity": row.get('How much Equity funding have you raised? \n\nAnswer in Rupees \nmention 0 in case of NA'),
            "Debt": row.get('How much Debt funding have you raised?\n\n*Answer in Rupees \nmention 0 in case of NA*'),
            "Grants": row.get('How much Grant funding have you raised?\n\n*Answer in Rupees\nmention 0 in case of NA*'),
            "VideoURL": row.get("Add the video here"),
            "Language": row.get("Language"),
            "Nooffounders": row.get("Number of founders (in numbers)"),
            "TeamSize": row.get("TeamSize"),
            "City": row.get("City/District"),
            "State": row.get("State"),
            "Foundingyear": row.get("When did you start this company? "),
            "Application Date": datetime.datetime.strptime(row.get("Timestamp"), "%m/%d/%Y %H:%M:%S") ,
            'source': 'Google Form'
        }
        return formattedRow


def syncData(sheetName: str):
    from .models import Startup
    from search.models import Source

    # if not is_sheet_updated(sheetName):
    #     print(f"Sheet {sheetName} is up to date")
    #     return


    # If sheet is updated
    rows = get_all_rows(sheetName)
    from pprint import pprint
    # print(rows)
    for row in rows:

        row = getFormattedRow(row, sheetName)
        if not row:
            continue

        mobileNumber = str(row.get("Mobile Number")).replace(' ', '')


        if not mobileNumber:
            continue
        if not row.get('Company'):
            continue
        mobileNumber = mobileNumber.lstrip('0')
        
        if len(mobileNumber) > 10:
            mobileNumber = mobileNumber[-10:]
        
        try:
            Startup.objects.get(mobile_number=mobileNumber)
            print("ALready",mobileNumber)
            continue
        except Startup.DoesNotExist:
            pass
        try:
            Startup.objects.get(additional_number=mobileNumber)
            print("ALready",mobileNumber)
            continue
        except Startup.DoesNotExist:
            pass

        currentStatus = None

        status = row.get("Current Status").lower()

    

        if not status or 'review' in status:
            currentStatus = 'in_review'
        elif 'r1' in status:
            if 'pre' in status:
                currentStatus = 'pre_r1_stage'
            elif 'conduct' in status:
                currentStatus = 'to_conduct_r1'
            else:
                currentStatus = 'r1'
        elif 'r2' in status:
            currentStatus = 'r2'
        elif 'visit' in status:
            currentStatus = 'site_visit'
        elif "reject" in status:
            currentStatus = 'rejected'
        elif "knockout" in status:
            currentStatus = 'knockout'
        
        currentSector = None
        subSector = None

        sector = row.get("Sector").lower()
        if 'waste' in sector:
            currentSector = 'waste_management'
        elif 'supply' in sector:
            currentSector = 'supply_chain'
        elif 'mobility' in sector:
            currentSector = 'mobility'
        elif 'agriculture' in sector:
            currentSector = 'agriculture'
        elif 'health' in sector:
            currentSector = 'health'
        elif 'financial' in sector:
            currentSector = 'financial_inclusion'
        else:
            currentSector = 'other'
            subSector = sector

        if row.get('SubSector'):
            subSector = row.get('SubSector')
        application_date = None
        if row.get('Application Date'):
            application_date = row.get('Application Date')

        source, created = Source.objects.get_or_create(name=row["source"])
        
        if subSector and len(subSector)> 200:
            subSector = None

        try:
            startup_instance = Startup(
                name=get_value_or_none(row, 'Company'),
                mobile_number=mobileNumber if mobileNumber else None,
                founder_name=get_value_or_none(row, 'Founder'),
                about=get_value_or_none(row, 'About'),
                current_status=currentStatus if currentStatus else None,
                sector=currentSector,
                sub_sector=subSector,
                ARR=get_value_or_none(row, "12MRevenue"),
                equity=get_value_or_none(row, 'Equity'),
                debt=get_value_or_none(row, 'Debt'),
                grants=get_value_or_none(row, 'Grants'),
                video_url=get_value_or_none(row, 'VideoURL'),
                language=get_value_or_none(row, 'Language'),
                no_of_founders=get_value_or_none(row, 'Nooffounders'),
                team_size=get_value_or_none(row, 'TeamSize'),
                city=get_value_or_none(row, 'City'),
                state=get_value_or_none(row, 'State'),
                founding_year=get_value_or_none(row, 'Foundingyear'),
                application_date=application_date if application_date else datetime.datetime.now(),
                source_name=row['source'],
                source=source,
                source_type="INBOUND",
            )
            print(f"Saving {startup_instance.name}")
            startup_instance.save()

        except Exception as e:
                # startup_as_dict = {
                # "name": row.get('Company'),
                # "mobile_number": mobileNumber,
                # "founder_name": row.get('Founder'),
                # "about": row.get('About'),
                # "current_status": currentStatus,
                # "sector": row.get('Sector'),
                # "ARR": row.get("12MRevenue"),
                # "equity": row.get('Equity'),
                # "debt": row.get('Debt'),
                # "grants": row.get('Grants'),
                # "video_url": row.get('VideoURL'),
                # "language": row.get('Language'),
                # "no_of_founders": row.get('Nooffounders'),
                # "team_size": row.get('TeamSize'),
                # "city": row.get('City'),
                # "state": row.get('State'),
                # "founding_year": row.get('Foundingyear'),
                # "application_date": datetime.datetime.now().isoformat(),
                # }
                # print(f"Error in creating instance for {startup_as_dict}")
                print(f"Error Creating Startup Instance {e}")
                pprint(row)

                break
        
        


def syncDataTemp(sheetName: str):
    from .models import Startup
    from search.models import Source

    # if not is_sheet_updated(sheetName):
    #     print(f"Sheet {sheetName} is up to date")
    #     return


    # If sheet is updated
    rows = get_all_rows(sheetName)
    from pprint import pprint
    # print(rows)
    for row in rows:
        row = {    
            **row,
            "source": "Notion"
        }   
        

        mobileNumber = str(row.get("Mobile Number")).replace(' ', '')


        # if not mobileNumber:
        #     continue
        if not row.get('Company'):
            continue
        mobileNumber = mobileNumber.lstrip('0')
        
        if len(mobileNumber) > 10:
            mobileNumber = mobileNumber[-10:]
        
        try:
            Startup.objects.get(name=row.get('Company'))
            print("ALready",row.get('Company'))
            continue
        except Startup.DoesNotExist:
            pass

        currentStatus = None

        status = row.get("Current Status",'').lower()
        currentStage = None
        stage = row.get("Stage")

        if stage:
            stage = stage.lower()
        print(stage, "*"*10)
        if not stage:
            currentStage = None
        elif 'seed+' in stage:
            currentStage = 'seed+'
        elif 'seed' in stage:
            currentStage = 'seed'
        elif 'seriesa' in stage:
            currentStage = 'series_a'
        elif 'seriesb' in stage:
            currentStage = 'series_b'
        elif 'pre-seed' in stage:
            currentStage = 'pre_seed'
        elif 'idea' in stage:
            currentStage = 'idea_stage'
        elif 'pre-seriesa' in stage:
            currentStage = 'pre_series_a'
        elif 'series c' in stage or 'series c and above' in stage:
            currentStage = 'series_c_and_above'
        print(currentStage)
        # breakpoint()
    
        if not status or 'review' in status:
            currentStatus = 'in_review'
        elif 'r1' in status:
            if 'pre' in status:
                currentStatus = 'pre_r1_stage'
            elif 'conduct' in status:
                currentStatus = 'to_conduct_r1'
            else:
                currentStatus = 'r1'
        elif 'r2' in status:
            currentStatus = 'r2'
        elif 'visit' in status:
            currentStatus = 'site_visit'
        elif "reject" in status:
            currentStatus = 'rejected'
        elif "monitor" in status:
            currentStatus = 'monitor'
        elif "knockout" in status:
            currentStatus = 'knockout'
        
        commentpp = row.get("Rejection Comments")
        currentSector = None
        subSector = None

        sector = row.get("Sector").lower()
        if 'waste' in sector:
            currentSector = 'waste_management'
        elif 'supply' in sector:
            currentSector = 'supply_chain'
        elif 'mobility' in sector:
            currentSector = 'mobility'
        elif 'agriculture' in sector:
            currentSector = 'agriculture'
        elif 'health' in sector:
            currentSector = 'health'
        elif 'financial' in sector:
            currentSector = 'financial_inclusion'
        else:
            currentSector = 'other'
            subSector = sector

        if row.get('SubSector'):
            subSector = row.get('SubSector')
        application_date = None
        if row.get('Application Date'):
            application_date = row.get('Application Date')

        poc = row.get('POC').replace(' ','').lower().split(',')
        if poc:
            poc = poc[0]
        from django.contrib.auth.models import User
        owner = None
        ownera = User.objects.filter(username__icontains=poc)

        if ownera:
            owner = ownera[0]

        source, created = Source.objects.get_or_create(name=row["source"])
        
        if subSector and len(subSector)> 200:
            subSector = None
        nom = row.get('Nominator')
        source_name=row['source']
        source_type="INBOUND"
        if nom:
            source_type="OUTBOUND"
            source_name=nom

        try:
            startup_instance = Startup(
                name=get_value_or_none(row, 'Company'),
                mobile_number=mobileNumber if mobileNumber else None,
                founder_name=get_value_or_none(row, 'Founder'),
                about=get_value_or_none(row, 'About'),
                current_status=currentStatus if currentStatus else None,
                sector=currentSector,
                sub_sector=subSector,
                ARR=get_value_or_none(row, "12MRevenue"),
                equity=get_value_or_none(row, 'Equity'),
                debt=get_value_or_none(row, 'Debt'),
                grants=get_value_or_none(row, 'Grants'),
                video_url=get_value_or_none(row, 'VideoURL'),
                language=get_value_or_none(row, 'Language'),
                no_of_founders=get_value_or_none(row, 'Nooffounders'),
                team_size=get_value_or_none(row, 'TeamSize'),
                city=get_value_or_none(row, 'City'),
                state=get_value_or_none(row, 'State'),
                founding_year=get_value_or_none(row, 'Foundingyear'),
                application_date=application_date if application_date else datetime.datetime.now(),
                source_name=source_name,
                source=source,
                source_type=source_type,
                stage=currentStage,
                deal_owner=owner,
                rejected_comment=commentpp
            )
            # breakpoint()
            print(f"Saving {startup_instance.name}")
            startup_instance.save()

        except Exception as e:
                # startup_as_dict = {
                # "name": row.get('Company'),
                # "mobile_number": mobileNumber,
                # "founder_name": row.get('Founder'),
                # "about": row.get('About'),
                # "current_status": currentStatus,
                # "sector": row.get('Sector'),
                # "ARR": row.get("12MRevenue"),
                # "equity": row.get('Equity'),
                # "debt": row.get('Debt'),
                # "grants": row.get('Grants'),
                # "video_url": row.get('VideoURL'),
                # "language": row.get('Language'),
                # "no_of_founders": row.get('Nooffounders'),
                # "team_size": row.get('TeamSize'),
                # "city": row.get('City'),
                # "state": row.get('State'),
                # "founding_year": row.get('Foundingyear'),
                # "application_date": datetime.datetime.now().isoformat(),
                # }
                # print(f"Error in creating instance for {startup_as_dict}")
                print(f"Error Creating Startup Instance {e}")
                pprint(row)

                break
        