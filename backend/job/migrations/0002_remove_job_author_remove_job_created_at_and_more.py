# Generated by Django 5.1.1 on 2024-10-05 19:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('job', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='job',
            name='author',
        ),
        migrations.RemoveField(
            model_name='job',
            name='created_at',
        ),
        migrations.RemoveField(
            model_name='job',
            name='industry',
        ),
        migrations.RemoveField(
            model_name='job',
            name='job_type',
        ),
        migrations.RemoveField(
            model_name='job',
            name='location',
        ),
        migrations.RemoveField(
            model_name='job',
            name='post_status',
        ),
    ]
