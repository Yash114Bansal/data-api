# Generated by Django 4.2.13 on 2024-07-30 14:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('search', '0052_startup_rejection_message_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='startup',
            name='rejection_message',
            field=models.CharField(blank=True, max_length=600, null=True, verbose_name='Rejection Message'),
        ),
    ]
