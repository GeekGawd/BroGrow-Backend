# Generated by Django 4.0.4 on 2022-12-30 11:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('map', '0004_loanapplication_financial_data'),
    ]

    operations = [
        migrations.AddField(
            model_name='loanapplication',
            name='created_at',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
