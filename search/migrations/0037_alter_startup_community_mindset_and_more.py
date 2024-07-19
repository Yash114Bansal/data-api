# Generated by Django 4.2.13 on 2024-07-19 12:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('search', '0036_alter_startup_community_mindset_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='startup',
            name='community_mindset',
            field=models.CharField(choices=[('yes', 'Yes'), ('no', 'No'), ('na', 'N/A')], default='na', help_text='Will they give their time to someone they don`t know, who is seeking advice?', max_length=3, verbose_name='Community Mindset'),
        ),
        migrations.AlterField(
            model_name='startup',
            name='fund_alignment',
            field=models.CharField(choices=[('yes', 'Yes'), ('no', 'No'), ('na', 'N/A')], default='na', help_text='Is their business model directly increasing the income of India 2 or India 3?', max_length=3, verbose_name='Fund Alignment'),
        ),
        migrations.AlterField(
            model_name='startup',
            name='intent_driven',
            field=models.CharField(choices=[('yes', 'Yes'), ('no', 'No'), ('na', 'N/A')], default='-', help_text='Are they Intent driven?', max_length=3, verbose_name='Intent Driven'),
        ),
        migrations.AlterField(
            model_name='startup',
            name='systemic_change_potential',
            field=models.CharField(choices=[('yes', 'Yes'), ('no', 'No'), ('na', 'N/A')], default='na', help_text='If their business succeeds, will they continue to seek other ways to help solve the same social problem?', max_length=3, verbose_name='Systemic Change Potential'),
        ),
    ]
