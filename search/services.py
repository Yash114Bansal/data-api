import datetime
import os
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




def is_sheet_updated(doc_name: str) :
    client = settings.GSPREAD_CLIENT
    sh = client.open(doc_name)
    props = sh.fetch_sheet_metadata()  # Example function to fetch metadata
    # print(props)
    modifiedTime = client.get_file_drive_metadata(props["spreadsheetId"]).get("modifiedTime")
    # sheet_last_modified = datetime.datetime.strptime(props['modifiedTime'], '%Y-%m-%dT%H:%M:%S.%fZ')
    print(modifiedTime)
    return modifiedTime 

def get_value_or_none(row, field):
    value = row.get(field)
    return value if value else None


def syncData():
    from .models import Company, Startup

    sheetName = "Next Bharat Residency Program- WhatsApp Bot data"
    # TODO check if sheet is updated or not

    # If sheet is updated
    rows = get_all_rows(sheetName)
    from pprint import pprint
    # print(rows)
    for row in rows:
        mobileNumber = str(row.get("Mobile Number"))

        if not mobileNumber:
            continue
        if not row.get('Company'):
            continue

        mobileNumber = mobileNumber[2:]
        try:
            Startup.objects.get(phone_number=mobileNumber)
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
            
        try:
            startup_instance = Startup(
                name=get_value_or_none(row, 'Company'),
                phone_number=mobileNumber if mobileNumber else None,
                founder_name=get_value_or_none(row, 'Founder'),
                about=get_value_or_none(row, 'About'),
                current_status=currentStatus if currentStatus else None,
                sector=get_value_or_none(row, 'Sector'),
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
                application_date=datetime.datetime.now(),
            )

        except:
                startup_as_dict = {
                "name": row.get('Company'),
                "mobile_number": mobileNumber,
                "founder_name": row.get('Founder'),
                "about": row.get('About'),
                "current_status": currentStatus,
                "sector": row.get('Sector'),
                "ARR": row.get("12MRevenue"),
                "equity": row.get('Equity'),
                "debt": row.get('Debt'),
                "grants": row.get('Grants'),
                "video_url": row.get('VideoURL'),
                "language": row.get('Language'),
                "no_of_founders": row.get('Nooffounders'),
                "team_size": row.get('TeamSize'),
                "city": row.get('City'),
                "state": row.get('State'),
                "founding_year": row.get('Foundingyear'),
                "application_date": datetime.datetime.now().isoformat(),
                }
                # print(f"Error in creating instance for {startup_as_dict}")
                print(row)

                break
        print(f"Saving {startup_instance.name}")
        startup_instance.save()

        # print(f"Saved {startup_instance.name}") 
