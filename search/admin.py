from django.contrib import admin
from django.contrib.auth import get_user_model
from django.utils import timezone
from datetime import timedelta
from extras.models import OtherCompanyInfo
from .models import Company, Director, GSTData, Source, Startup, StartupStatusCounts, Team
from django.db.models import Count, Q
from django.utils.html import format_html
User = get_user_model()


@admin.register(StartupStatusCounts)
class StartupCountAdmin(admin.ModelAdmin):
    change_list_template = 'admin/status.html'

    def changelist_view(self, request, extra_context=None):
        response = super().changelist_view(request, extra_context=extra_context)

        if hasattr(response, 'context_data'):
            # Calculate the most recent Saturday
            today = timezone.now().date()
            last_saturday = today - timedelta(days=(today.weekday() + 2) % 7)

            # Overall status counts
            status_choices = dict(Startup.STATUS_CHOICES)

            # Get overall counts
            status_counts = Startup.objects.values('current_status').annotate(count=Count('id'))
            status_counts_dict = {item['current_status']: item['count'] for item in status_counts}
            
            # Initialize counts for all statuses to ensure all are present
            overall_counts = {status: status_counts_dict.get(status, 0) for status in status_choices.keys()}
            # Counts for each status since the last Saturday
            last_week_done = {
                'in_review': Startup.objects.filter(in_review_date__gte=last_saturday).count(),
                'pre_r1_stage': Startup.objects.filter(pre_r1_stage_date__gte=last_saturday).count(),
                'r1': Startup.objects.filter(r1_date__gte=last_saturday).count(),
                'r2': Startup.objects.filter(r2_date__gte=last_saturday).count(),
                'site_visit': Startup.objects.filter(site_visit_date__gte=last_saturday).count(),
                'rejected': Startup.objects.filter(rejected_date__gte=last_saturday).count(),
            }

            response.context_data['status_counts'] = overall_counts
            response.context_data['last_week_done'] = last_week_done

        return response

    def has_add_permission(self, request):
        return False  # Disable the ability to add new objects

    def has_change_permission(self, request, obj=None):
        return False  # Disable the ability to change existing objects

    def has_delete_permission(self, request, obj=None):
        return False  # Disable the ability to delete objects

class DirectorInline(admin.StackedInline):
    model = Director
    extra = 1
    fields = ('din', 'name', 'designation', 'date_of_appointment', 'address', 'pan', 'no_of_companies', 'father_name', 'dob', 'masked_aadhaar', 'phone_number', 'company_list', 'other_director_info', 'is_sole_proprietor', 'split_address')
    readonly_fields = ('din', 'name')

@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ('cin', 'name', 'incorporation_date', 'last_agm_date', 'status')
    search_fields = ('cin', 'name', 'status')
    list_filter = ('status', 'incorporation_date', 'last_agm_date')
    inlines = [DirectorInline]
    fields = (
        'cin', 'name', 'incorporation_date', 'last_agm_date', 'registration_number', 'registered_address',
        'balance_sheet_date', 'category', 'sub_category', 'company_class', 'company_type', 'paid_up_capital',
        'authorised_capital', 'status', 'roc_office', 'country_of_incorporation', 'description_of_main_division',
        'email_id', 'address_other_than_registered_office', 'number_of_members', 'active_compliance',
        'suspended_at_stock_exchange', 'nature_of_business', 'status_for_efiling', 'status_under_cirp', 'pan',
    )
    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        if not request.user.is_superuser:
            queryset = queryset.filter(startup__deal_owner=request.user)
        return queryset

    def save_model(self, request, obj, form, change):
        obj.last_edited_by = request.user
        super().save_model(request, obj, form, change)

class OtherCompanyInfoInline(admin.StackedInline):
    model = OtherCompanyInfo
    can_delete = False
    verbose_name_plural = 'Other Company Info'

@admin.register(Startup)
class StartupAdmin(admin.ModelAdmin):
    list_display = ('name', 'founder_name', 'sector', 'current_status', 'last_edited_on')
    search_fields = ('name', 'founder_name', 'sector', 'current_status')
    list_filter = ('current_status', 'sector', 'last_edited_on')

    fieldsets = (
        ('Main Info', {
                'fields': ('legal_entity', 'name', 'mobile_number', 'founder_name', 'about', 'no_of_founders', 
                        'team_size', 'city', 'state', 'sector', 'ARR', 'founding_year', 'equity', 'debt', 
                        'grants', 'video_url', 'language', 'current_status', 'last_edited_by', 
                        'attachment1', 'attachment2', 'attachment3', 'relevant_link1', 'relevant_link2', 
                        'relevant_link3', 'deal_owner', 'deal_viewer', 'source','source_type' ,'source_name','email', 
                        'phone_number','intent_driven', 'fund_alignment', 'community_mindset', 'systemic_change_potential'),
            }),
        ('Comments', {
                'fields': ('in_review_comment', 'pre_r1_stage_comment', 'r1_comment', 'r2_comment', 
                        'site_visit_comment', 'rejected_comment', 'notes', 'additional_comments', ),
            }),
        ('Dates', {
                'fields': ('application_date', 'in_review_date', 'pre_r1_stage_date', 'r1_date', 'r2_date', 
                        'site_visit_date', 'rejected_date', 'last_edited_on'),
            }),
            
    )
    inlines = [OtherCompanyInfoInline]
    
    readonly_fields = (
        'in_review_date', 'pre_r1_stage_date', 'r1_date', 'r2_date', 'site_visit_date', 
        'rejected_date', 'last_edited_on', 'last_edited_by'
    )
    def formfield_for_dbfield(self, db_field, **kwargs):
        formfield = super().formfield_for_dbfield(db_field, **kwargs)
        if db_field.name in ['attachment1', 'attachment2', 'attachment3', 'video_url']:
            request = kwargs.get('request')
            if request and request.path.endswith('/change/'):
                obj = self.get_object(request, request.resolver_match.kwargs['object_id'])
                if obj:
                    if db_field.name == 'video_url':
                        url = getattr(obj, 'video_url')
                    else:
                        url = getattr(obj, db_field.name).url if getattr(obj, db_field.name) else None
                    if url:
                        preview_html = self.get_preview_html(url)
                        original_render = formfield.widget.render

                        def custom_render(name, value, attrs=None, renderer=None):
                            input_html = original_render(name, value, attrs, renderer)
                            return format_html('{}<br>{}', preview_html, input_html)

                        formfield.widget.render = custom_render

        return formfield

    def get_preview_html(self, url):
        if url.endswith(('.mp4', '.mov', '.avi', '.wmv')):
            return format_html('<video width="600" controls><source src="{}" type="video/mp4">Your browser does not support the video tag.</video>', url)
        
        elif url.endswith('.pdf'):
            return format_html(
                '''
                <a href="{}" target="_blank" onclick="window.open('{}', 'PDF', 'width=800,height=600'); return false;" 
                style="display: inline-block; padding: 10px 20px; font-size: 16px; color: white; background-color: #007bff; border: none; border-radius: 5px; text-decoration: none; text-align: center;">
                Open PDF</a>
                ''', url, url
            )
        
        else:
            return ''
    
    def get_readonly_fields(self, request, obj=None):
        readonly_fields = list(self.readonly_fields)
        # breakpoint()
        if request.user.is_superuser or request.user == obj.deal_owner:
            return readonly_fields
        elif request.user in obj.deal_viewer.members.all():
            # return readonly_fields
            return [field.name for field in obj._meta.fields ]
        else:
            return readonly_fields
    
    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        if not request.user.is_superuser:
            queryset = queryset.filter(
                Q(deal_owner=request.user) | Q(deal_viewer__members=request.user)
            ).distinct()

        return queryset

    def save_model(self, request, obj, form, change):
        obj.last_edited_by = request.user
        super().save_model(request, obj, form, change)
    def render_change_form(self, request, context, add=False, change=False, form_url='', obj=None):
        context.update({
            'show_save': True,
            'show_save_and_continue': False,
            'show_save_and_add_another': False,
            'show_delete': True
        })
        return super().render_change_form(request, context, add, change, form_url, obj)


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
admin.site.register(Team)