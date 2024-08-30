from django.db import models

class Accelerator(models.Model):
    unique_id = models.CharField(max_length=100, blank=True, null=True)
    email = models.CharField(max_length=100, blank=True, null=True)
    phone = models.CharField(max_length=30, blank=True, null=True)
    pan = models.CharField(max_length=20, blank=True, null=True)
    role = models.CharField(max_length=100, blank=True, null=True)
    company_name = models.CharField(max_length=200, blank=True, null=True)
    date_of_establishment = models.CharField(max_length=200, blank=True, null=True)
    country = models.CharField(max_length=100, blank=True, null=True)
    state = models.CharField(max_length=100, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    industry = models.TextField(blank=True, null=True)
    sectors = models.TextField(blank=True, null=True)
    first_name = models.CharField(max_length=100, blank=True, null=True)
    last_name = models.CharField(max_length=100, blank=True, null=True)
    designation = models.CharField(max_length=100, blank=True, null=True)
    email_id = models.CharField(max_length=100, blank=True, null=True)
    mobile_number = models.CharField(max_length=30, blank=True, null=True)
    landline_number = models.CharField(max_length=30, blank=True, null=True)
    website = models.CharField(max_length=300, blank=True, null=True)
    social_media_url = models.CharField(max_length=300, blank=True, null=True)

    def __str__(self):
        return self.company_name

class Incubator(models.Model):
    unique_id = models.CharField(max_length=100, blank=True, null=True)
    email = models.CharField(max_length=100, blank=True, null=True)
    phone = models.CharField(max_length=30, blank=True, null=True)
    pan = models.CharField(max_length=20, blank=True, null=True)
    role = models.CharField(max_length=100, blank=True, null=True)
    company_name = models.CharField(max_length=200, blank=True, null=True)
    country = models.CharField(max_length=100, blank=True, null=True)
    state = models.CharField(max_length=100, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    industry = models.TextField(blank=True, null=True)
    sectors = models.TextField(blank=True, null=True)
    incubation_centers_locations = models.TextField(blank=True, null=True)
    first_name = models.CharField(max_length=100, blank=True, null=True)
    last_name = models.CharField(max_length=100, blank=True, null=True)
    designation = models.CharField(max_length=100, blank=True, null=True)
    email_id = models.CharField(max_length=100, blank=True, null=True)
    mobile_number = models.CharField(max_length=30, blank=True, null=True)
    landline_number = models.CharField(max_length=30, blank=True, null=True)
    website = models.CharField(max_length=300, blank=True, null=True)
    social_media_url = models.CharField(max_length=300, blank=True, null=True)

    def __str__(self):

        return self.company_name
    