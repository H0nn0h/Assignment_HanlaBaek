# Generated by Django 5.1.1 on 2024-09-17 21:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Maungawhau', '0014_remove_collegeday_date_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='collegeday',
            name='attendance_status',
        ),
    ]
