# Generated by Django 3.2.9 on 2023-03-10 16:32

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AccountType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, unique=True)),
                ('code', models.CharField(max_length=255, unique=True)),
            ],
            options={
                'db_table': 'ibedc_account_type',
            },
        ),
        migrations.CreateModel(
            name='BuildingDescription',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, unique=True)),
                ('code', models.CharField(max_length=255, unique=True)),
            ],
            options={
                'db_table': 'ibedc_building_description',
            },
        ),
        migrations.CreateModel(
            name='CaadVat',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, unique=True)),
                ('code', models.CharField(max_length=255, unique=True)),
            ],
            options={
                'db_table': 'ibedc_caad_vat',
            },
        ),
        migrations.CreateModel(
            name='CustomerCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, unique=True)),
                ('code', models.CharField(max_length=255, unique=True)),
            ],
            options={
                'db_table': 'ibedc_customer_category',
            },
        ),
        migrations.CreateModel(
            name='CustomerType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, unique=True)),
                ('code', models.CharField(max_length=255, unique=True)),
            ],
            options={
                'db_table': 'ibedc_customer_type',
            },
        ),
        migrations.CreateModel(
            name='PremiseType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, unique=True)),
                ('code', models.CharField(max_length=255, unique=True)),
            ],
            options={
                'db_table': 'ibedc_premise_type',
            },
        ),
        migrations.CreateModel(
            name='ServiceBand',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, unique=True)),
                ('code', models.CharField(max_length=255, unique=True)),
            ],
            options={
                'db_table': 'ibedc_service_band',
            },
        ),
        migrations.CreateModel(
            name='SupplyType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, unique=True)),
                ('code', models.CharField(max_length=255, unique=True)),
            ],
            options={
                'db_table': 'ibedc_supply_type',
            },
        ),
        migrations.CreateModel(
            name='UserProcessHierarchy',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('process_code', models.CharField(max_length=255)),
                ('precedence', models.IntegerField(default=0)),
                ('position_code', models.CharField(max_length=255)),
            ],
            options={
                'db_table': 'ibedc_user_process_hierarchy',
            },
        ),
    ]
