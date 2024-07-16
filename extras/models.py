from django.db import models
from search.models import Startup

class OtherCompanyInfo(models.Model):
    # Basic Information
    startup = models.OneToOneField(Startup, on_delete=models.SET_NULL,blank=True, null=True)
    age_of_company = models.PositiveIntegerField(
        help_text="Number of years since the company was founded.", blank=True, null=True
    )
    founders_and_team = models.TextField(
        help_text="Names and roles of the founders and key team members.", blank=True, null=True
    )
    
    # Background
    story_of_founder = models.TextField(
        help_text="Personal and professional background of the founder.", blank=True, null=True
    )
    about_the_company = models.TextField(
        help_text="General information about the company.", blank=True, null=True
    )
    
    # Market
    market_landscape = models.TextField(
        help_text="Description of the market landscape in which the company operates.", blank=True, null=True
    )
    market_size = models.CharField(
        max_length=255,
        help_text="Estimated size of the market.", blank=True, null=True
    )
    problem_being_solved = models.TextField(
        help_text="The problem the company aims to solve.", blank=True, null=True
    )
    
    # Business Model
    solution_business_model = models.TextField(
        help_text="Description of the solution or business model, including any revenue-generating activities.", blank=True, null=True
    )
    revenue_generating_activities = models.TextField(
        help_text="Activities through which the company generates revenue.", blank=True, null=True
    )
    revenue_streams = models.TextField(
        help_text="Different streams of revenue for the company.", blank=True, null=True
    )
    
    # Performance Metrics
    traction = models.TextField(
        help_text="Key performance indicators and impact of the company.", blank=True, null=True
    )
    unit_economics = models.TextField(
        help_text="Details on the unit economics of the business.", blank=True, null=True
    )
    business_trajectory = models.TextField(
        help_text="Business trajectory over the last 2-3 years.", blank=True, null=True
    )
    
    # Competition and Funding
    competition = models.TextField(
        help_text="Information about the competition.", blank=True, null=True
    )
    total_funding_raised = models.DecimalField(
        max_digits=20, decimal_places=2,
        help_text="Total amount of funding raised by the company.", blank=True, null=True
    )
    investors = models.TextField(
        help_text="Names of the investors.", blank=True, null=True
    )
    
    # Achievements and Future Plans
    achievements_and_recognition = models.TextField(
        help_text="Achievements and recognition received by the company.", blank=True, null=True
    )
    fund_requirement = models.DecimalField(
        max_digits=20, decimal_places=2,
        help_text="Amount of funding required.", blank=True, null=True
    )
    fund_utilisation = models.TextField(
        help_text="Plan for the utilisation of the funds.", blank=True, null=True
    )
    next_plan = models.TextField(
        help_text="Future plans of the company.", blank=True, null=True
    )
    
    # SWOT Analysis
    positives = models.TextField(
        help_text="Strengths or positive aspects of the company.", blank=True, null=True
    )
    concerns_risks = models.TextField(
        help_text="Concerns or risks associated with the company.", blank=True, null=True
    )
    
    # Strategic Information
    genesis_of_startup = models.TextField(
        help_text="Explanation of why the startup was founded.", blank=True, null=True
    )
    is_business_impact_first = models.BooleanField(
        default=False,
        help_text="Indicates if the business prioritizes impact over other objectives.", blank=True, null=True
    )
    reason_for_business_not_non_profit = models.TextField(
        help_text="Reason for choosing a business model instead of a non-profit model.", blank=True, null=True
    )
    pivots_in_business_journey = models.TextField(
        help_text="Details of any pivots made in the business journey and the reasons behind them, especially if decisions were made to retain impact.", blank=True, null=True
    )
    
    # Beneficiary Information
    beneficiary_role = models.CharField(
        max_length=255,
        help_text="Role of the beneficiary in the value chain, such as customer, employee, etc.", blank=True, null=True
    )
    
    def __str__(self):
        return self.about_the_company[:50]  # Short description for admin display
