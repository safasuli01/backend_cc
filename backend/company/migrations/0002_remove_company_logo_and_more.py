# Generated by Django 5.1.1 on 2024-10-04 13:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('company', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='company',
            name='logo',
        ),
        migrations.RemoveField(
            model_name='company',
            name='registration_document',
        ),
    ]
