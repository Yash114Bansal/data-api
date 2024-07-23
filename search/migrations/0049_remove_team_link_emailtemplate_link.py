# Generated by Django 4.2.13 on 2024-07-23 11:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('search', '0048_remove_directinvestment_source_type_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='team',
            name='link',
        ),
        migrations.AddField(
            model_name='emailtemplate',
            name='link',
            field=models.URLField(blank=True, null=True, verbose_name='Calendly Link'),
        ),
    ]
