# Generated by Django 3.2.9 on 2023-03-25 01:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0002_auto_20230325_0226'),
    ]

    operations = [
        migrations.AddField(
            model_name='usertasksinbox',
            name='associated_customer',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
