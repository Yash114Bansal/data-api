# Generated by Django 4.2.13 on 2024-08-06 03:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('search', '0054_alter_startup_application_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='startup',
            name='application_date',
            field=models.DateField(blank=True, null=True),
        ),
    ]
