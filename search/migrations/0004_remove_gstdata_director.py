# Generated by Django 4.2.13 on 2024-07-06 13:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('search', '0003_director_is_sole_proprietor_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='gstdata',
            name='director',
        ),
    ]
