# Generated by Django 3.2.9 on 2023-03-20 20:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('payments', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ecmitransactions',
            name='transref',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='payments.ecmipaymenthistory'),
        ),
    ]