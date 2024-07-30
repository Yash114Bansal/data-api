from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.core.exceptions import ValidationError


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
    # link = models.URLField(max_length=200, blank=True, null=True, verbose_name='Calendly Link')

    def __str__(self) -> str:
        return self.name

class EmailTemplate(models.Model):
    STATUS_CHOICES = [
        ('in_review', 'In-review'),
        ('pre_r1_stage', 'Pre-R1 stage'),
        ('r1', 'R1'),
        ('scheduled_r1', 'To conduct R1'),
        ('r2', 'R2'),
        ("pre_ic", "Pre-IC"),
        ('ic', 'IC'),
        ('site_visit', 'Site visit'),
        ('approved_for_investments', 'Approved for investments'),
        ('approved_for_residency', 'Approved for residency'),
        ('monitor', 'Monitor'),
        ('rejected', 'Rejected'),
        ('knockout', 'Knockout')
    ]

    status = models.CharField(max_length=50, choices=STATUS_CHOICES, unique=True)
    subject = models.CharField(max_length=255)
    body = models.TextField()

    def __str__(self) -> str:
        return self.status

class Startup(models.Model):
    # New fields for specific statuses
    STATUS_CHOICES = [
        ('in_review', 'In-review'),
        ('pre_r1_stage', 'Pre-R1 stage'),
        ('r1', 'R1'),
        ('scheduled_r1', 'Scheduled R1'),
        ('site_visit', 'Site visit'),
        ('r2', 'R2'),
        ("pre_ic", "Pre-IC"),
        ('ic', 'IC'),
        ('approved_for_investments', 'Approved for investments'),
        ('approved_for_residency', 'Approved for residency'),
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
    YES_NO_CHOICES = (
        ('yes', 'Yes'),
        ('no', 'No'),
        ('na', 'N/A'),
    )
    legal_entity = models.OneToOneField(Company,on_delete=models.SET_NULL,blank=True, null=True)
    name = models.CharField(max_length=200, null=True, blank=True)
    mobile_number = models.CharField(max_length=15, null=True, blank=True)
    founder_name = models.CharField(max_length=200, null=True, blank=True)
    about = models.TextField(blank=True, null=True)
    current_status = models.CharField(max_length=50, choices=STATUS_CHOICES, blank=True, null=True)
    stage = models.CharField(max_length=50, choices=STAGE_CHOICES, blank=True, null=True)
    additional_comments = models.TextField(blank=True, null=True)
    attachment1 = models.FileField(upload_to='attachments/', blank=True, null=True, verbose_name='Additional Attachment')
    attachment2 = models.FileField(upload_to='attachments/', blank=True, null=True, verbose_name='Additional Attachment')
    pitch_deck = models.FileField(upload_to='attachments/', blank=True, null=True)
    website = models.URLField(max_length=200, blank=True, null=True)
    relevant_link1 = models.URLField(max_length=200, blank=True, null=True, verbose_name='Additional Link')
    relevant_link2 = models.URLField(max_length=200, blank=True, null=True, verbose_name='Additional Link')
    deal_owner = models.ForeignKey(User, related_name='deal_companies', blank=True, on_delete=models.SET_NULL, null=True)
    deal_viewer = models.ForeignKey(Team, blank=True, null=True,on_delete=models.SET_NULL)
    last_edited_by = models.ForeignKey(User, related_name='edited_companies', on_delete=models.SET_NULL, blank=True, null=True)
    source = models.ForeignKey(Source, on_delete=models.SET_NULL, blank=True, null=True)
    source_name = models.CharField(max_length=200,null=True, blank=True)

    # Fields for specific statuses
    approved_for_investments_comment = models.TextField(blank=True, null=True, verbose_name="Approved For Investments")
    approved_for_residency_comment = models.TextField(blank=True, null=True, verbose_name="Approved For Residency")
    ic_comment = models.TextField(blank=True, null=True, verbose_name="IC")
    pre_ic_comment = models.TextField(blank=True, null=True, verbose_name="Pre IC")
    pre_r1_stage_comment = models.TextField(blank=True, null=True, verbose_name="Pre-Rround 1 Stage")
    r1_comment = models.TextField(blank=True, null=True, verbose_name="Round 1")
    r2_comment = models.TextField(blank=True, null=True, verbose_name="Round 2")
    site_visit_comment = models.TextField(blank=True, null=True, verbose_name="Site Visit")
    monitor_comment = models.TextField(blank=True, null=True, verbose_name="Monitor")
    rejected_comment = models.TextField(blank=True, null=True, verbose_name="Rejected")

    approved_for_investments_date = models.DateField(
        blank=True, null=True, verbose_name="Approved for Investments"
    )
    approved_for_residency_date = models.DateField(
        blank=True, null=True, verbose_name="Approved for Residency"
    )
    in_review_date = models.DateField(
        blank=True, null=True, verbose_name="In Review"
    )
    ic_date = models.DateField(
        blank=True, null=True, verbose_name="IC"
    )
    pre_ic_date = models.DateField(
        blank=True, null=True, verbose_name="Pre-IC"
    )
    pre_r1_stage_date = models.DateField(
        blank=True, null=True, verbose_name="Pre-Round 1 Stage"
    )
    r1_date = models.DateField(
        blank=True, null=True, verbose_name="Round 1"
    )
    r2_date = models.DateField(
        blank=True, null=True, verbose_name="Round 2"
    )
    site_visit_date = models.DateField(
        blank=True, null=True, verbose_name="Site Visit"
    )
    site_visited_date = models.DateField(
        blank=True, null=True, verbose_name="Site Visited"
    )
    scheduled_r1_date = models.DateField(
        blank=True, null=True, verbose_name="Scheduled R1 Date"
    )
    monitor_date = models.DateField(
        blank=True, null=True, verbose_name="Monitor"
    )
    rejected_date = models.DateField(
        blank=True, null=True, verbose_name="Rejected"
    )
    knockout_date = models.DateField(
        blank=True, null=True, verbose_name="Knockout"
    )

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
    additional_number = models.CharField(max_length=10, blank=True, null=True)
    
    # Yes NO Questions


    intent_driven = models.CharField(
        verbose_name='Intent Driven',
        help_text='Are they Intent driven?',
        choices=YES_NO_CHOICES,
        max_length=3,
        default='na',
    )

    fund_alignment = models.CharField(
        verbose_name='Fund Alignment',
        help_text='Is their business model directly increasing the income of India 2 or India 3?',
        choices=YES_NO_CHOICES,
        max_length=3,
        default='na',
    )

    community_mindset = models.CharField(
        verbose_name='Community Mindset',
        help_text='Will they give their time to someone they don`t know, who is seeking advice?',
        choices=YES_NO_CHOICES,
        max_length=3,
        default='na',
    )

    systemic_change_potential = models.CharField(
        verbose_name='Systemic Change Potential',
        help_text='If their business succeeds, will they continue to seek other ways to help solve the same social problem?',
        choices=YES_NO_CHOICES,
        max_length=3,
        default='na',
    )
    # def clean(self):
        # valid_transitions = {
        #     'in_review': ['scheduled_r1', 'pre_r1_stage','knockout', 'r1', 'rejected', 'monitor'],
        #     'scheduled_r1': ['pre_r1_stage', 'knockout', 'r1', 'rejected', 'monitor'],
        #     'pre_r1_stage': ['r1', 'rejected', 'monitor'],
        #     'r1': ['r2', 'rejected', 'monitor'],
        #     'r2': ['site_visit', 'rejected', 'monitor'],
        #     'site_visit': ['pre_ic', 'rejected', 'monitor'],
        #     'pre_ic': ['ic', 'rejected', 'monitor'],
        #     'ic': ['approved_for_investments', 'approved_for_residency', 'rejected', 'monitor'],
        #     'approved_for_investments': ['monitor', 'rejected', 'approved_for_residency', 'monitor'],
        #     'approved_for_residency': ['monitor', 'rejected', 'approved_for_investments', 'monitor'],
        #     'monitor': ['rejected'],
        #     'rejected': [],
        #     'knockout': []
        # }

        # if self.pk:
        #     previous_status = Startup.objects.get(pk=self.pk).current_status
        #     if previous_status != self.current_status :

        #         # try:
        #         #     EmailTemplate.objects.get(status=self.current_status)
        #         # except EmailTemplate.DoesNotExist:
        #         #     raise ValidationError(f"Email template not found for status {self.current_status}")
                
        #         # this is to check if the status transition is valid
        #         # if previous_status and self.current_status not in valid_transitions[previous_status]:
        #         #     raise ValidationError(f"Invalid status transition from {previous_status} to {self.current_status}")
                
        #         if not self.deal_viewer:
        #             raise ValidationError(f"Deal Viewers not set")


    def save(self, *args, **kwargs):
        # self.clean()
        status_date_mapping = {
            'in_review': 'in_review_date',
            'pre_r1_stage': 'pre_r1_stage_date',
            'r1': 'r1_date',
            'r2': 'r2_date',
            'pre_ic': 'pre_ic_date',
            'ic': 'ic_date',
            'site_visit': 'site_visit_date',
            'approved_for_residency': 'approved_for_residency_date',
            'approved_for_investments': 'approved_for_investments_date',
            'scheduled_r1': 'scheduled_r1_date',
            'monitor': 'monitor_date',
            'rejected': 'rejected_date',
            'knockout': 'knockout_date'
        }

        if self.current_status in status_date_mapping:
            setattr(self, status_date_mapping[self.current_status], timezone.now().date())
        super().save(*args, **kwargs)
    
    def __str__(self) -> str:
        return self.name if self.name else 'Unnamed Startup'
    
    class Meta:
        verbose_name = "Program application"
        verbose_name_plural = "Program applications"

class DirectInvestment(models.Model):
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
        ('scheduled_r1', 'Scheduled R1'),
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
    YES_NO_CHOICES = (
        ('yes', 'Yes'),
        ('no', 'No'),
        ('na', 'N/A'),
    )
    legal_entity = models.OneToOneField(Company,on_delete=models.SET_NULL,blank=True, null=True)
    name = models.CharField(max_length=200, null=True, blank=True)
    mobile_number = models.CharField(max_length=15, null=True, blank=True)
    founder_name = models.CharField(max_length=200, null=True, blank=True)
    about = models.TextField(blank=True, null=True)
    current_status = models.CharField(max_length=50, choices=STATUS_CHOICES, blank=True, null=True)
    stage = models.CharField(max_length=50, choices=STAGE_CHOICES, blank=True, null=True)
    additional_comments = models.TextField(blank=True, null=True)
    attachment1 = models.FileField(upload_to='attachments/', blank=True, null=True, verbose_name='Additional Attachment')
    attachment2 = models.FileField(upload_to='attachments/', blank=True, null=True, verbose_name='Additional Attachment')
    pitch_deck = models.FileField(upload_to='attachments/', blank=True, null=True)
    website = models.URLField(max_length=200, blank=True, null=True)
    relevant_link1 = models.URLField(max_length=200, blank=True, null=True, verbose_name='Additional Link')
    relevant_link2 = models.URLField(max_length=200, blank=True, null=True, verbose_name='Additional Link')
    deal_owner = models.ForeignKey(User, related_name='deal_directinv', blank=True, on_delete=models.SET_NULL, null=True)
    deal_viewer = models.ForeignKey(Team, blank=True, null=True,on_delete=models.SET_NULL)
    last_edited_by = models.ForeignKey(User, related_name='edited_directinv', on_delete=models.SET_NULL, blank=True, null=True)
    source = models.ForeignKey(Source, on_delete=models.SET_NULL, blank=True, null=True)
    source_name = models.CharField(max_length=200,null=True, blank=True)

    # Fields for specific statuses
    approved_for_investments_comment = models.TextField(blank=True, null=True, verbose_name="Approved For Investments")
    approved_for_residency_comment = models.TextField(blank=True, null=True, verbose_name="Approved For Residency")
    ic_comment = models.TextField(blank=True, null=True, verbose_name="IC")
    pre_ic_comment = models.TextField(blank=True, null=True, verbose_name="Pre IC")
    pre_r1_stage_comment = models.TextField(blank=True, null=True, verbose_name="Pre-Rround 1 Stage")
    r1_comment = models.TextField(blank=True, null=True, verbose_name="Round 1")
    r2_comment = models.TextField(blank=True, null=True, verbose_name="Round 2")
    site_visit_comment = models.TextField(blank=True, null=True, verbose_name="Site Visit")
    monitor_comment = models.TextField(blank=True, null=True, verbose_name="Monitor")
    rejected_comment = models.TextField(blank=True, null=True, verbose_name="Rejected")

    approved_for_investments_date = models.DateField(
        blank=True, null=True, verbose_name="Approved for Investments"
    )
    approved_for_residency_date = models.DateField(
        blank=True, null=True, verbose_name="Approved for Residency"
    )
    in_review_date = models.DateField(
        blank=True, null=True, verbose_name="In Review"
    )
    ic_date = models.DateField(
        blank=True, null=True, verbose_name="IC"
    )
    pre_ic_date = models.DateField(
        blank=True, null=True, verbose_name="Pre-IC"
    )
    pre_r1_stage_date = models.DateField(
        blank=True, null=True, verbose_name="Pre-Round 1 Stage"
    )
    r1_date = models.DateField(
        blank=True, null=True, verbose_name="Round 1"
    )
    r2_date = models.DateField(
        blank=True, null=True, verbose_name="Round 2"
    )
    site_visit_date = models.DateField(
        blank=True, null=True, verbose_name="Site Visit"
    )
    site_visited_date = models.DateField(
        blank=True, null=True, verbose_name="Site Visited"
    )
    scheduled_r1_date = models.DateField(
        blank=True, null=True, verbose_name="To Conduct Round 1"
    )
    monitor_date = models.DateField(
        blank=True, null=True, verbose_name="Monitor"
    )
    rejected_date = models.DateField(
        blank=True, null=True, verbose_name="Rejected"
    )
    knockout_date = models.DateField(
        blank=True, null=True, verbose_name="Knockout"
    )

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
    additional_number = models.CharField(max_length=10, blank=True, null=True)
    
    # Yes NO Questions


    intent_driven = models.CharField(
        verbose_name='Intent Driven',
        help_text='Are they Intent driven?',
        choices=YES_NO_CHOICES,
        max_length=3,
        default='na',
    )

    fund_alignment = models.CharField(
        verbose_name='Fund Alignment',
        help_text='Is their business model directly increasing the income of India 2 or India 3?',
        choices=YES_NO_CHOICES,
        max_length=3,
        default='na',
    )

    community_mindset = models.CharField(
        verbose_name='Community Mindset',
        help_text='Will they give their time to someone they don`t know, who is seeking advice?',
        choices=YES_NO_CHOICES,
        max_length=3,
        default='na',
    )

    systemic_change_potential = models.CharField(
        verbose_name='Systemic Change Potential',
        help_text='If their business succeeds, will they continue to seek other ways to help solve the same social problem?',
        choices=YES_NO_CHOICES,
        max_length=3,
        default='na',
    )

    def save(self, *args, **kwargs):
        status_date_mapping = {
            'approved_for_investments': 'approved_for_investments_date',
            'approved_for_residency': 'approved_for_residency_date',
            'in_review': 'in_review_date',
            'ic': 'ic_date',
            'site_visit': 'site_visit_date',
            'pre_ic': 'pre_ic_date',
            'pre_r1_stage': 'pre_r1_stage_date',
            'r1': 'r1_date',
            'r2': 'r2_date',
            'scheduled_r1': 'scheduled_r1_date',
            'monitor': 'monitor_date',
            'rejected': 'rejected_date',
            'knockout': 'knockout_date'
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
        verbose_name = 'Dashboard'
        verbose_name_plural = 'Dashboard'



