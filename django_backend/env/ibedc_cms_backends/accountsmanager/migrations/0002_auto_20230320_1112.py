# Generated by Django 3.2.9 on 2023-03-20 10:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accountsmanager', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='customerdrafts',
            options={'managed': False},
        ),
        migrations.AlterModelOptions(
            name='customereditqueue',
            options={'managed': False},
        ),
    ]