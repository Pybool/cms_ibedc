# Generated by Django 3.2.9 on 2023-03-10 16:40

import authentication.models
from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='AuthGroup',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150, unique=True)),
            ],
            options={
                'db_table': 'auth_group',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('name', models.CharField(default='Name N/A', max_length=255)),
                ('email', models.EmailField(max_length=255, unique=True, verbose_name='email address')),
                ('phone1', models.CharField(default='Name N/A', max_length=255)),
                ('phone2', models.CharField(default='Name N/A', max_length=255)),
                ('twitter_handle', models.CharField(default='Name N/A', max_length=255)),
                ('user_type', models.CharField(choices=[('Admin', 'Admin'), ('Regular', 'Regular'), ('Visitor', 'Visitor')], default='Regular', max_length=100)),
                ('bio', models.TextField(blank=True, default='N/A')),
                ('slug', models.SlugField(editable=False, unique=True)),
                ('administration', models.CharField(default='', max_length=255)),
                ('active', models.BooleanField(blank=True, null=True)),
                ('action_id', models.IntegerField(blank=True, null=True)),
                ('suspend_user', models.CharField(blank=True, max_length=200, null=True)),
                ('permission_hierarchy', models.CharField(blank=True, max_length=200, null=True)),
                ('region', models.CharField(blank=True, max_length=200, null=True)),
                ('business_unit', models.CharField(blank=True, max_length=200, null=True)),
                ('service_center', models.CharField(blank=True, max_length=200, null=True)),
                ('can_approve', models.BooleanField(blank=True, default=False, null=True)),
                ('bucode', models.CharField(blank=True, max_length=200, null=True)),
                ('can_manage_2fa', models.BooleanField(blank=True, default=False, null=True)),
                ('position', models.CharField(blank=True, max_length=200, null=True)),
                ('can_approve_caad', models.BooleanField(blank=True, default=False, null=True)),
                ('can_create_user', models.BooleanField(blank=True, default=False, null=True)),
                ('can_create_customer', models.BooleanField(blank=True, default=False, null=True)),
                ('is_dev', models.BooleanField(default=False, null=True)),
                ('avatar', models.FileField(blank=True, null=True, upload_to='user_avatar')),
                ('otp', models.IntegerField(blank=True, default=None, null=True, validators=[django.core.validators.MinValueValidator(100000), django.core.validators.MaxValueValidator(999999)])),
                ('otp_expires_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('is_verified_account', models.BooleanField(default=False)),
                ('is_staff', models.BooleanField(default=True)),
                ('is_regularuser', models.BooleanField(default=True)),
                ('is_superuser', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('last_login', models.DateTimeField(blank=True, null=True)),
                ('updated_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('enable_2fa', models.BooleanField(default=False, verbose_name='Two Factor Authentication')),
                ('secret_code_2fa', models.CharField(blank=True, max_length=255, null=True, verbose_name='Two Factor Authentication Secret Code')),
                ('qr_image_2fa', models.BinaryField(blank=True, max_length='max', null=True, verbose_name='Two Factor Authentication QR Code')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'abstract': False,
            },
            managers=[
                ('objects', authentication.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='ResetPassword',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.CharField(max_length=255)),
                ('otp', models.CharField(blank=True, max_length=255, null=True)),
                ('reset_password_token', models.CharField(max_length=255, unique=True)),
                ('otp_expires_at', models.DateTimeField(default='2000-01-01 01:01:30.475275')),
            ],
        ),
        migrations.CreateModel(
            name='UserJWTtokens',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_id', models.IntegerField()),
                ('token', models.CharField(max_length=255)),
                ('createdAt', models.DateTimeField(auto_now_add=True)),
                ('expiredAt', models.DateTimeField()),
            ],
        ),
        migrations.CreateModel(
            name='UsersLog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_date', models.DateTimeField(blank=True, null=True)),
                ('write_date', models.DateTimeField(blank=True, null=True)),
                ('create_uid', models.ForeignKey(blank=True, db_column='create_uid', null=True, on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL)),
                ('write_uid', models.ForeignKey(blank=True, db_column='write_uid', null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='users_log_update', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='UserprocessHierarchy',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('process_code', models.CharField(blank=True, max_length=30, null=True)),
                ('position_code', models.CharField(blank=True, max_length=30, null=True)),
                ('create_date', models.DateTimeField(blank=True, null=True)),
                ('write_date', models.DateTimeField(blank=True, null=True)),
                ('precedence', models.IntegerField(blank=True, null=True)),
                ('create_uid', models.ForeignKey(blank=True, db_column='create_uid', null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='cuph', to=settings.AUTH_USER_MODEL)),
                ('write_uid', models.ForeignKey(blank=True, db_column='write_uid', null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='updateuph', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='UserPreferences',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('billing_main_page', models.CharField(blank=True, max_length=1000, null=True)),
                ('payments_main_page', models.CharField(blank=True, max_length=1000, null=True)),
                ('personal_info_page', models.CharField(blank=True, max_length=1000, null=True)),
                ('cust_billing_page', models.CharField(blank=True, max_length=1000, null=True)),
                ('cust_payment_page', models.CharField(blank=True, max_length=1000, null=True)),
                ('cust_metering_page', models.CharField(blank=True, max_length=1000, null=True)),
                ('cust_assets_page', models.CharField(blank=True, max_length=1000, null=True)),
                ('create_date', models.DateTimeField(blank=True, null=True)),
                ('write_date', models.DateTimeField(blank=True, null=True)),
                ('customerstransientviews', models.CharField(blank=True, max_length=1000, null=True)),
                ('create_uid', models.ForeignKey(blank=True, db_column='create_uid', null=True, on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL)),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='user', to=settings.AUTH_USER_MODEL)),
                ('write_uid', models.ForeignKey(blank=True, db_column='write_uid', null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='users_pref_updated', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='UserPositions',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=200, null=True, unique=True)),
                ('code', models.CharField(blank=True, max_length=200, null=True, unique=True)),
                ('position_code', models.CharField(blank=True, max_length=200, null=True)),
                ('create_date', models.DateTimeField(blank=True, null=True)),
                ('write_date', models.DateTimeField(blank=True, null=True)),
                ('create_uid', models.ForeignKey(blank=True, db_column='create_uid', null=True, on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL)),
                ('write_uid', models.ForeignKey(blank=True, db_column='write_uid', null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='users_pos_update', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
