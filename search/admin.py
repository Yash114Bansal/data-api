from django.contrib import admin
from django.contrib.auth import get_user_model
from django.utils import timezone
from datetime import timedelta

import requests
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
                'approved_for_residency': Startup.objects.filter(approved_for_residency_date__gte=last_saturday).count(),
                'approved_for_investments': Startup.objects.filter(approved_for_investments_date__gte=last_saturday).count(),
                'in_review': Startup.objects.filter(in_review_date__gte=last_saturday).count(),
                'pre_r1_stage': Startup.objects.filter(pre_r1_stage_date__gte=last_saturday).count(),
                'ic': Startup.objects.filter(ic_date__gte=last_saturday).count(),
                'pre_ic': Startup.objects.filter(pre_ic_date__gte=last_saturday).count(),
                'r1': Startup.objects.filter(r1_date__gte=last_saturday).count(),
                'r2': Startup.objects.filter(r2_date__gte=last_saturday).count(),
                'site_visit': Startup.objects.filter(site_visit_date__gte=last_saturday).count(),
                'to_conduct_r1': Startup.objects.filter(to_conduct_r1_date__gte=last_saturday).count(),
                'monitor': Startup.objects.filter(monitor_date__gte=last_saturday).count(),
                'rejected': Startup.objects.filter(rejected_date__gte=last_saturday).count(),
                'knockout': Startup.objects.filter(knockout_date__gte=last_saturday).count(),
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
    verbose_name_plural = 'Additional Details'

@admin.register(Startup)
class StartupAdmin(admin.ModelAdmin):
    list_display = ('name', 'founder_name', 'sector', 'ARR', 'current_status','source_name' )
    search_fields = ('name', 'founder_name', 'sector', 'current_status')
    list_filter = ('current_status', 'deal_owner', 'sector')

    fieldsets = (
        ('Main', {
                'fields': ('legal_entity', 'name','website' , 'founder_name', 'mobile_number', 'additional_number', 'email',  'about', 'no_of_founders', 
                        'team_size', 'city', 'state', 'sector', 'sub_sector' ,'ARR', 'founding_year', 'equity', 'debt', 
                        'grants', 'video_url', 'relevant_link1', 'relevant_link2','pitch_deck', 'attachment1', 'attachment2', 
                        'source','source_type' ,'source_name', 'language','stage' ,'current_status',
                        'intent_driven', 'fund_alignment', 'community_mindset', 'systemic_change_potential' ,'deal_owner', 'deal_viewer','last_edited_by', ),
            }),
            ('Internal Notes', {
                'fields': (
                    'pre_r1_stage_comment','r1_comment', 'r2_comment', 'site_visit_comment','pre_ic_comment',  'ic_comment',  
                    'approved_for_residency_comment', 'approved_for_investments_comment', 
                    'rejected_comment', 'monitor_comment', 'additional_comments',
                ),
            }),
            ('Timeline', {
                'fields': (
                    'application_date', 'pre_r1_stage_date', 'r1_date', 'r2_date', 'site_visit_date', 'site_visited_date','pre_ic_date','ic_date', 
                    'approved_for_investments_date', 'approved_for_residency_date',  
                    'knockout_date', 'rejected_date', 'monitor_date','last_interaction_date','last_edited_on' 
                ),
            }),
            
    )
    inlines = [OtherCompanyInfoInline]
    
    readonly_fields = (
            'in_review_date', 'pre_r1_stage_date', 'r1_date', 'r2_date', 'site_visit_date',
            'rejected_date', 'last_edited_on', 'last_edited_by',
            'approved_for_investments_date', 'approved_for_residency_date', 'ic_date', 
            'pre_ic_date', 'to_conduct_r1_date', 'monitor_date', 'knockout_date'
        )
    def formfield_for_dbfield(self, db_field, **kwargs):
        formfield = super().formfield_for_dbfield(db_field, **kwargs)
        if db_field.name in ['attachment1', 'attachment2', 'pitch_deck', 'video_url']:
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
    
    def is_video_url(self, url):
        # Check for common video file extensions in the URL
        video_extensions = ('.mp4', '.avi', '.mov', '.mkv', '.flv', '.wmv', '.webm')
        if url.lower().endswith(video_extensions):
            return True

        # Check the Content-Type header to confirm it's a video
        try:
            response = requests.head(url, allow_redirects=True)
            content_type = response.headers.get('Content-Type', '')
            if 'video' in content_type:
                return True
        except requests.RequestException as e:
            print(f"An error occurred: {e}")

        return False
    def get_preview_html(self, url):
        if self.is_video_url(url):
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
    
    # def get_readonly_fields(self, request, obj=None):
    #     readonly_fields = list(self.readonly_fields)
    #     # breakpoint()
    #     if request.user.is_superuser or request.user == obj.deal_owner:
    #         return readonly_fields
    #     elif request.user in obj.deal_viewer.members.all():
    #         # return readonly_fields
    #         return [field.name for field in obj._meta.fields ]
    #     else:
    #         return readonly_fields
    
    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        if not request.user.is_superuser:
            queryset = queryset.filter(
                Q(deal_owner=request.user) | Q(deal_viewer__members=request.user)
            ).distinct()

        return queryset

    def save_model(self, request, obj, form, change):
        obj.last_edited_by = request.user
        if not request.user.is_superuser:
            obj.deal_owner = request.user
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