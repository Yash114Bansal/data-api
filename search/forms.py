from django import forms

class CompanySearchForm(forms.Form):
    company_name = forms.CharField(label='Company Name', max_length=100)
