from django.contrib import admin
from django.contrib.auth import get_user_model
from .models import Company, Director, GSTData, Source

User = get_user_model()

class DirectorInline(admin.StackedInline):
    model = Director
    extra = 1
    fields = ('din', 'name', 'designation', 'date_of_appointment', 'address', 'pan', 'no_of_companies', 'father_name', 'dob', 'masked_aadhaar', 'phone_number', 'company_list', 'other_director_info', 'is_sole_proprietor', 'split_address')
    readonly_fields = ('din', 'name')

@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ('cin', 'name', 'incorporation_date', 'last_agm_date', 'status','current_status')
    search_fields = ('cin', 'name', 'status')
    list_filter = ('status', 'incorporation_date', 'last_agm_date','current_status')
    inlines = [DirectorInline]
    fields = (
        'cin', 'name', 'incorporation_date', 'last_agm_date', 'registration_number', 'registered_address',
        'balance_sheet_date', 'category', 'sub_category', 'company_class', 'company_type', 'paid_up_capital',
        'authorised_capital', 'status', 'roc_office', 'country_of_incorporation', 'description_of_main_division',
        'email_id', 'address_other_than_registered_office', 'number_of_members', 'active_compliance',
        'suspended_at_stock_exchange', 'nature_of_business', 'status_for_efiling', 'status_under_cirp', 'pan',
        'current_status', 'status_comment', 'notes', 'additional_comments', 'attachment1', 'attachment2',
        'attachment3', 'relevant_link1', 'relevant_link2', 'relevant_link3', 'deal_owner', 'last_edited_by',
        'in_review_comment', 'pre_r1_stage_comment', 'r1_comment', 'r2_comment', 'site_visit_comment', 'rejected_comment',
        'in_review_date', 'pre_r1_stage_date', 'r1_date', 'r2_date', 'site_visit_date', 'rejected_date','sector',
        'twelve_m_revenue', 'equity', 'debt', 'grants', 'video_url','language','source'
    )
    readonly_fields = ('in_review_date', 'pre_r1_stage_date', 'r1_date', 'r2_date', 'site_visit_date', 'rejected_date', 'last_edited_by')

    def save_model(self, request, obj, form, change):
        obj.last_edited_by = request.user
        super().save_model(request, obj, form, change)

@admin.register(Director)
class DirectorAdmin(admin.ModelAdmin):
    list_display = ('din', 'name', 'designation', 'date_of_appointment', 'company')
    search_fields = ('din', 'name', 'designation', 'company__name')
    list_filter = ('designation', 'date_of_appointment', 'company')

@admin.register(GSTData)
class GSTDataAdmin(admin.ModelAdmin):
    list_display = ('gst_no', 'year', 'gst_estimated_total', 'gst_filed_total', 'company_name')
    search_fields = ('gst_no', 'year', 'company_name')
    list_filter = ('year', 'gst_status')

admin.site.register(Source)