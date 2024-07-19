from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone



class Source(models.Model):
    name = models.CharField(max_length=200, unique=True)

    def __str__(self) -> str:
        return self.name
    
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

    class Meta:
        verbose_name_plural = "Companies"

    def __str__(self) -> str:
        return f"{self.name} || {self.cin}"

class Team(models.Model):
    name = models.CharField(max_length=200, unique=True)
    members = models.ManyToManyField(User)

    def __str__(self) -> str:
        return self.name

class Startup(models.Model):
    # New fields for specific statuses
    STATUS_CHOICES = [
        ('approved_for_investments', 'Approved for investments'),
        ('approved_for_residency', 'Approved for residency'),
        ('in_review', 'In-review'),
        ('pre_r1_stage', 'Pre-R1 stage'),
        ('ic', 'IC'),
        ("pre_ic", "Pre-IC"),
        ('r1', 'R1'),
        ('r2', 'R2'),
        ('site_visit', 'Site visit'),
        ('to_conduct_r1', 'To conduct R1'),
        ('monitor', 'Monitor'),
        ('rejected', 'Rejected'),
        ('knockout', 'Knockout')
    ]
    SECTOR_CHOICES = [
        ('other', "Other"),
        ('waste_management', "Waste Management"),
        ('supply_chain', "Supply Chain"),
        ('mobility', "Mobility"),
        ('agriculture', "Agriculture"),
        ('health', "Health"),
        ('financial_inclusion', "Financial Inclusion"),
    ]
    INBOUND_OUTBOUND_CHOICES = [
    ('INBOUND', 'Inbound'),
    ('OUTBOUND', 'Outbound'),
    ]
    STAGE_CHOICES = [
        ('idea', "Idea"),
        ('pre_seed', "Pre-seed"),
        ('seed', "Seed"),
        ('seed+', "Seed+"),
        ('pre_series_a', "Pre-series A"),
        ('series_a', "Series A"),
        ('series_b', "Series B"),
        ('series_c_and_above', "Series C and above"),
    ]
    legal_entity = models.OneToOneField(Company,on_delete=models.SET_NULL,blank=True, null=True)
    name = models.CharField(max_length=200, null=True, blank=True)
    mobile_number = models.CharField(max_length=15, null=True, blank=True)
    founder_name = models.CharField(max_length=200, null=True, blank=True)
    about = models.TextField(blank=True, null=True)
    current_status = models.CharField(max_length=50, choices=STATUS_CHOICES, blank=True, null=True)
    stage = models.CharField(max_length=50, choices=STAGE_CHOICES, blank=True, null=True)
    additional_comments = models.TextField(blank=True, null=True)
    attachment1 = models.FileField(upload_to='attachments/', blank=True, null=True)
    attachment2 = models.FileField(upload_to='attachments/', blank=True, null=True)
    pitch_deck = models.FileField(upload_to='attachments/', blank=True, null=True)
    website = models.URLField(max_length=200, blank=True, null=True)
    relevant_link1 = models.URLField(max_length=200, blank=True, null=True)
    relevant_link2 = models.URLField(max_length=200, blank=True, null=True)
    deal_owner = models.ForeignKey(User, related_name='deal_companies', blank=True, on_delete=models.SET_NULL, null=True)
    deal_viewer = models.ForeignKey(Team, blank=True, null=True,on_delete=models.SET_NULL)
    last_edited_by = models.ForeignKey(User, related_name='edited_companies', on_delete=models.SET_NULL, blank=True, null=True)
    source = models.ForeignKey(Source, on_delete=models.SET_NULL, blank=True, null=True)
    source_name = models.CharField(max_length=200,null=True, blank=True)

    # Fields for specific statuses
    approved_for_investments_comment = models.TextField(blank=True, null=True)
    approved_for_residency_comment = models.TextField(blank=True, null=True)
    in_review_comment = models.TextField(blank=True, null=True)
    ic_comment = models.TextField(blank=True, null=True)
    pre_ic_comment = models.TextField(blank=True, null=True)
    pre_r1_stage_comment = models.TextField(blank=True, null=True)
    r1_comment = models.TextField(blank=True, null=True)
    r2_comment = models.TextField(blank=True, null=True)
    site_visit_comment = models.TextField(blank=True, null=True)
    to_conduct_r1_comment = models.TextField(blank=True, null=True)
    monitor_comment = models.TextField(blank=True, null=True)
    rejected_comment = models.TextField(blank=True, null=True)

    approved_for_investments_date = models.DateField(blank=True, null=True)
    approved_for_residency_date = models.DateField(blank=True, null=True)
    in_review_date = models.DateField(blank=True, null=True)
    ic_date = models.DateField(blank=True, null=True)
    pre_ic_date = models.DateField(blank=True, null=True)
    pre_r1_stage_date = models.DateField(blank=True, null=True)
    r1_date = models.DateField(blank=True, null=True)
    r2_date = models.DateField(blank=True, null=True)
    site_visit_date = models.DateField(blank=True, null=True)
    to_conduct_r1_date = models.DateField(blank=True, null=True)
    monitor_date = models.DateField(blank=True, null=True)
    rejected_date = models.DateField(blank=True, null=True)
    knockout_date = models.DateField(blank=True, null=True)
    last_interaction_date = models.DateField(blank=True, null=True)

    sector = models.CharField(max_length=100, choices=SECTOR_CHOICES, blank=True, null=True)
    sub_sector = models.CharField(max_length=200, blank=True, null=True)
    ARR = models.CharField(max_length=200, blank=True, null=True)
    equity = models.CharField(max_length=200, blank=True, null=True)
    debt = models.CharField(max_length=200, blank=True, null=True)
    grants = models.CharField(max_length=200, blank=True, null=True)
    video_url = models.URLField(max_length=200,blank=True, null=True)
    language = models.CharField(max_length=50, blank=True, null=True)
    no_of_founders = models.CharField(max_length=200, blank=True, null=True)
    team_size = models.IntegerField(blank=True, null=True)
    city = models.CharField(max_length=200, blank=True, null=True)
    state = models.CharField(max_length=100, blank=True, null=True)
    founding_year = models.CharField(max_length=200,blank=True, null=True)
    application_date = models.DateField(blank=True, null=True)
    last_edited_on = models.DateTimeField(auto_now=True)
    email = models.EmailField(null=True, blank=True)
    phone_number = models.CharField(max_length=10, blank=True, null=True)
    
    source_type = models.CharField(
        max_length=8,
        choices=INBOUND_OUTBOUND_CHOICES,
        blank=True,
        null=True
    )
    # Yes NO Questions

    intent_driven = models.BooleanField(
        verbose_name='Intent Driven',
        help_text='Are they Intent driven?', blank=True, null=True
    )
    fund_alignment = models.BooleanField(
        verbose_name='Fund Alignment',
        help_text='Is their business model directly increasing the income of India 2 or India 3?',blank=True, null=True
    )
    community_mindset = models.BooleanField(
        verbose_name='Community Mindset',
        help_text='Will they give their time to someone they don`t know, who is seeking advice?',blank=True, null=True
    )
    systemic_change_potential = models.BooleanField(
        verbose_name='Systemic Change Potential',
        help_text='If their business succeeds, will they continue to seek other ways to help solve the same social problem?',blank=True, null=True
    )

    def save(self, *args, **kwargs):
        status_date_mapping = {
            'in_review': 'in_review_date',
            'pre_r1_stage': 'pre_r1_stage_date',
            'r1': 'r1_date',
            'r2': 'r2_date',
            'site_visit': 'site_visit_date',
            'rejected': 'rejected_date',
        }
        if self.current_status in status_date_mapping:
            setattr(self, status_date_mapping[self.current_status], timezone.now().date())
        super().save(*args, **kwargs)
    
    def __str__(self) -> str:
        return self.name if self.name else 'Unnamed Startup'

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
    masked_aadhaar = models.CharField(max_length=50, blank=True, null=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    company_list = models.JSONField(blank=True, null=True)

    other_director_info = models.JSONField(blank=True, null=True) # Contains GST Numbers
    is_sole_proprietor = models.CharField(max_length=15, blank=True, null=True)


    split_address = models.CharField(max_length=1000, blank=True, null=True)


    def __str__(self) -> str:
        return f"{self.name} || {self.company.name} || {self.din}"
    
    


class GSTData(models.Model):
    gst_no = models.CharField(max_length=50, blank=True, null=True)
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
    company_name = models.CharField(max_length=1000, blank=True, null=True)

    class Meta:
        unique_together = ('gst_no', 'year')
    def __str__(self) -> str:
        return f"{self.gst_no} || {self.year} || {self.company_name} "
    

class StartupStatusCounts(Startup):
    class Meta:
        proxy = True
        verbose_name = 'Startup Status Counts'
        verbose_name_plural = 'Startup Status Counts'

