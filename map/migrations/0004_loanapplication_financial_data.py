# Generated by Django 4.0.4 on 2022-12-29 18:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('map', '0003_loanapplication'),
    ]

    operations = [
        migrations.AddField(
            model_name='loanapplication',
            name='financial_data',
            field=models.JSONField(blank=True, null=True),
        ),
    ]
