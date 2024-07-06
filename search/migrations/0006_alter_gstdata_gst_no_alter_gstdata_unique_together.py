# Generated by Django 4.2.13 on 2024-07-06 14:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('search', '0005_gstdata_company_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='gstdata',
            name='gst_no',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterUniqueTogether(
            name='gstdata',
            unique_together={('gst_no', 'year')},
        ),
    ]
