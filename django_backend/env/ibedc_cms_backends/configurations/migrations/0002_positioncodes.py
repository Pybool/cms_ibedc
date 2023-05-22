# Generated by Django 3.2.9 on 2023-04-21 09:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('configurations', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='PositionCodes',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, unique=True)),
            ],
            options={
                'db_table': 'user_position_codes',
            },
        ),
    ]