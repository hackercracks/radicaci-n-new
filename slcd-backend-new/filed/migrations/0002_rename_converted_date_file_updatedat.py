# Generated by Django 3.2.15 on 2023-03-20 14:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('filed', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='file',
            old_name='converted_date',
            new_name='updatedAt',
        ),
    ]
