# Generated by Django 3.2.9 on 2023-03-20 11:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('billing', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='emsbills',
            options={'managed': True, 'ordering': ('-billdate',)},
        ),
    ]