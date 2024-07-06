# Generated by Django 4.2.13 on 2024-07-06 11:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('search', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='director',
            name='company_list',
            field=models.JSONField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='director',
            name='masked_aadhaar',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='director',
            name='phone_number',
            field=models.CharField(blank=True, max_length=15, null=True),
        ),
    ]
