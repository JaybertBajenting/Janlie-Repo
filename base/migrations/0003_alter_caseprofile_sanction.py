# Generated by Django 5.0.4 on 2024-06-05 19:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0002_remove_caseprofile_caseid_caseprofile_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='caseprofile',
            name='sanction',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]