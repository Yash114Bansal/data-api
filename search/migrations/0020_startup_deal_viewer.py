# Generated by Django 4.2.13 on 2024-07-15 13:59

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('search', '0019_alter_team_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='startup',
            name='deal_viewer',
            field=models.ManyToManyField(blank=True, to=settings.AUTH_USER_MODEL),
        ),
    ]
