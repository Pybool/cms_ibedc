# Generated by Django 3.2.9 on 2023-03-10 16:32

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='LocationsPermissions',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('region', models.CharField(blank=True, max_length=250, null=True)),
                ('biz_hub', models.CharField(blank=True, max_length=250, null=True)),
                ('servicecenter', models.CharField(blank=True, max_length=250, null=True)),
                ('create_date', models.DateTimeField(blank=True, null=True)),
                ('write_date', models.DateTimeField(blank=True, null=True)),
                ('created_by', models.CharField(blank=True, max_length=250, null=True)),
                ('updated_by', models.CharField(blank=True, max_length=250, null=True)),
                ('rid', models.CharField(blank=True, max_length=250, null=True)),
                ('buid', models.CharField(blank=True, max_length=250, null=True)),
                ('scid', models.CharField(blank=True, max_length=250, null=True)),
                ('service_center_address', models.CharField(blank=True, max_length=250, null=True)),
            ],
            options={
                'db_table': 'location_locationpermissions',
                'managed': False,
            },
        ),
    ]
