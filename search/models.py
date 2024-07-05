from django.db import models

class Company(models.Model):
    cin = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=255, blank=True, null=True)
    incorporation_date = models.CharField(max_length=50, blank=True, null=True)
    last_agm_date = models.CharField(max_length=50, blank=True, null=True)
    registration_number = models.CharField(max_length=50, blank=True, null=True)
    registered_address = models.TextField(blank=True, null=True)
    balance_sheet_date = models.CharField(max_length=50, blank=True, null=True)
    category = models.CharField(max_length=100, blank=True, null=True)
    sub_category = models.CharField(max_length=100, blank=True, null=True)
    company_class = models.CharField(max_length=50, blank=True, null=True)
    company_type = models.CharField(max_length=50, blank=True, null=True)
    paid_up_capital = models.CharField(max_length=50, blank=True, null=True)
    authorised_capital = models.CharField(max_length=50, blank=True, null=True)
    status = models.CharField(max_length=50, blank=True, null=True)
    roc_office = models.CharField(max_length=100, blank=True, null=True)
    country_of_incorporation = models.CharField(max_length=50, blank=True, null=True)
    description_of_main_division = models.CharField(max_length=255, blank=True, null=True)
    email_id = models.EmailField(max_length=255, blank=True, null=True)
    address_other_than_registered_office = models.TextField(blank=True, null=True)
    number_of_members = models.CharField(max_length=50, blank=True, null=True)
    active_compliance = models.CharField(max_length=50, blank=True, null=True)
    suspended_at_stock_exchange = models.CharField(max_length=50, blank=True, null=True)
    nature_of_business = models.CharField(max_length=255, blank=True, null=True)
    status_for_efiling = models.CharField(max_length=50, blank=True, null=True)
    status_under_cirp = models.CharField(max_length=50, blank=True, null=True)
    pan = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self) -> str:
        return f"{self.name} || {self.cin}"

class Director(models.Model):
    company = models.ForeignKey(Company, related_name='directors', on_delete=models.CASCADE)
    din = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=255, blank=True, null=True)
    designation = models.CharField(max_length=100, blank=True, null=True)
    date_of_appointment = models.CharField(max_length=50, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    pan = models.CharField(max_length=50, blank=True, null=True)
    no_of_companies = models.IntegerField(default=0, blank=True, null=True)
    father_name = models.CharField(max_length=255, blank=True, null=True)
    dob = models.CharField(max_length=50, blank=True, null=True)
    split_address = models.CharField(max_length=1000, blank=True, null=True)

    def __str__(self) -> str:
        return f"{self.name} || {self.company.name} || {self.din}"


class GSTData(models.Model):
    director = models.ForeignKey(Director, related_name='gst_data', on_delete=models.CASCADE)
    gst_no = models.CharField(max_length=50, unique=True, blank=True, null=True)
    year = models.CharField(max_length=50, blank=True, null=True)
    gst_estimated_total = models.CharField(max_length=255, blank=True, null=True)
    gst_filed_total = models.CharField(max_length=255, blank=True, null=True)
    pan_estimated_total = models.CharField(max_length=255, blank=True, null=True)
    pan_filed_total = models.CharField(max_length=255, blank=True, null=True)
    gst_status = models.CharField(max_length=50, blank=True, null=True)
    legal_name = models.CharField(max_length=255, blank=True, null=True)
    trade_name = models.CharField(max_length=255, blank=True, null=True)
    register_date = models.CharField(max_length=50, blank=True, null=True)
    tax_payer_type = models.CharField(max_length=50, blank=True, null=True)
    authorized_signatory = models.CharField(max_length=1000, blank=True, null=True)
    business_nature = models.CharField(max_length=1000, blank=True, null=True)

    def __str__(self) -> str:
        return f"{self.gst_no} || {self.director.company.name}"