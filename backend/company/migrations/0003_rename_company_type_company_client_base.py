# Generated by Django 5.1.1 on 2024-10-05 20:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('company', '0002_remove_company_logo_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='company',
            old_name='company_type',
            new_name='client_base',
        ),
    ]
