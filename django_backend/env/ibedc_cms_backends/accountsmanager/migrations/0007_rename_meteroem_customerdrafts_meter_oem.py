# Generated by Django 3.2.9 on 2023-04-10 08:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accountsmanager', '0006_rename_meter_oem_customerdrafts_meteroem'),
    ]

    operations = [
        migrations.RenameField(
            model_name='customerdrafts',
            old_name='meteroem',
            new_name='meter_oem',
        ),
    ]