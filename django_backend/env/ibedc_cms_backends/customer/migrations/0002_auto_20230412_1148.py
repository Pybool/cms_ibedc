# Generated by Django 3.2.9 on 2023-04-12 10:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='ecmicustomersnew',
            options={'managed': True},
        ),
        
        migrations.AlterField(
            model_name='emscustomersnew',
            name='booknumber',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='emscustomersnew',
            name='buid',
            field=models.CharField(blank=True, db_column='BUID', max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='emscustomersnew',
            name='cat',
            field=models.CharField(blank=True, db_column='CAT', max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='emscustomersnew',
            name='distributionstation',
            field=models.CharField(blank=True, db_column='DistributionStation', max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='emscustomersnew',
            name='injectionstation',
            field=models.CharField(blank=True, db_column='InjectionStation', max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='emscustomersnew',
            name='institutioncode',
            field=models.CharField(blank=True, db_column='institutionCode', max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='emscustomersnew',
            name='methodofidentification',
            field=models.CharField(blank=True, db_column='MethodOfIdentification', max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='emscustomersnew',
            name='newtariffcode',
            field=models.CharField(blank=True, db_column='NewTariffCode', max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='emscustomersnew',
            name='organisationcode',
            field=models.CharField(blank=True, db_column='OrganisationCode', max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='emscustomersnew',
            name='statuscode',
            field=models.CharField(blank=True, db_column='StatusCode', max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='emscustomersnew',
            name='title',
            field=models.CharField(blank=True, db_column='Title', max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='emscustomersnew',
            name='transid',
            field=models.CharField(blank=True, db_column='TransID', max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='emscustomersnew',
            name='utid',
            field=models.CharField(blank=True, db_column='UTID', max_length=100, null=True),
        ),
    ]