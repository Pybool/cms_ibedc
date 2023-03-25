from django.db import models
from django.utils import timezone
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)

from django.core.exceptions import ValidationError
from django.utils.crypto import get_random_string
from django.core.validators import MaxValueValidator, MinValueValidator
from django.contrib.auth.models import PermissionsMixin
# from django.contrib.auth.models import User
from django.utils.text import slugify
import itertools, uuid
from django.urls import reverse
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token


import datetime

# Create your models here.

COUNTRY_CHOICES = (
    ("Albania", "Albania"),("Nigeria", "Nigeria"), ("Algeria", "Algeria"), ("Angola", "Angola"), ("Argentina", "Argentina"), ("Armenia", "Armenia"), ("Australia", "Australia"), ("Austria", "Austria"), ("Azerbaijan", "Azerbaijan"), ("Bahamas", "Bahamas"), ("Bahrain", "Bahrain"), ("Bangladesh", "Bangladesh"), ("Barbados", "Barbados"), ("Belarus", "Belarus"), ("Belgium", "Belgium"), ("Belivia", "Belivia"), ("Belize", "Belize"), ("Benin", "Benin"), ("Bosnia", "Bosnia"), ("Botswana", "Botswana"), ("Brazil", "Brazil"), ("Brunei", "Brunei"), ("Bulgaria", "Bulgaria"), ("Camaroon", "Camaroon"), ("Cambodia", "Cambodia"), ("Canada", "Canada"), ("Chile", "Chile"), ("Colombia", "Colombia"), ("Costa Rica", "Costa Rica"), ("Cote D'ivoire", "Cote D'ivoire"), ("Croatia", "Croatia"), ("Cyprus", "Cyprus"), ("Czech Repub", "Czech Repub"), ("Denmark", "Denmark"), ("Dominican Repub", "Dominican Repub"), ("Ecuador", "Ecuador"), ("Egypt", "Egypt"), ("El Salvador", "El Salvador"), ("Estonia", "Estonia"), ("Ethiopia", "Ethiopia"), ("Fiji", "Fiji"), ("Finland", "Finland"), ("France", "France"), ("Georgia", "Georgia"), ("Germany", "Germany"), ("Ghana", "Ghana"), ("Greece", "Greece"), ("Grenada", "Grenada"), ("Guatemala", "Guatemala"), ("Guinea", "Guinea"), ("Guyana", "Guyana"), ("Haiti", "Haiti"), ("Honduras", "Honduras"), ("Hungary", "Hungary"), ("Iceland", "Iceland"), ("India", "India"), ("Indonesia", "Indonesia"), ("Ireland", "Ireland"), ("Israel", "Israel"), ("Italy", "Italy"), ("Jamaica Mon", "Jamaica Mon"), ("Japan", "Japan"), ("Jordan", "Jordan"), ("Kazakhstan", "Kazakhstan"), ("Kenya", "Kenya"), ("Kuwait", "Kuwait"), ("Kyrgyzstan", "Kyrgyzstan"), ("Laos", "Laos"), ("Latvia", "Latvia"), ("Lebanon", "Lebanon"), ("Lesotho", "Lesotho"), ("Liberia", "Liberia"), ("Libya", "Libya"), ("Lithuania", "Lithuania"), ("Luxembourg", "Luxembourg"), ("Madagascar", "Madagascar"), ("Malawi", "Malawi"), ("Malaysia", "Malaysia"), ("Maldives", "Maldives"), ("Malta", "Malta"), ("Mauritania", "Mauritania"), ("Mauritius", "Mauritius"), ("Mexico", "Mexico"), ("Moldova", "Moldova"), ("Mongolia", "Mongolia"), ("Montenegro", "Montenegro"), ("Morocco", "Morocco"), ("Myanmar", "Myanmar"), ("N Macedonia", "N Macedonia"), ("Namibia", "Namibia"), ("Nepal", "Nepal"), ("Netherlands", "Netherlands"), ("New Zealand", "New Zealand"), ("Nicaragua", "Nicaragua"), ("Niger", "Niger"), ("Norway", "Norway"), ("Oman", "Oman"), ("Pakistan", "Pakistan"), ("Palestine", "Palestine"), ("Panama", "Panama"), ("Papua New Guinea", "Papua New Guinea"), ("Paraguay", "Paraguay"), ("Peru", "Peru"), ("Philippines", "Philippines"), ("Poland", "Poland"), ("Portugal", "Portugal"), ("Qatar", "Qatar"), ("Romania", "Romania"), ("Rwanda", "Rwanda"), ("Samoa", "Samoa"), ("Saudi Arabia", "Saudi Arabia"), ("Senegal", "Senegal"), ("Serbia", "Serbia"), ("Seychelles", "Seychelles"), ("Sierra Leon", "Sierra Leon"), ("Singapore", "Singapore"), ("Slovakia", "Slovakia"), ("Slovenia", "Slovenia"), ("Somalia", "Somalia"), ("South Africa", "South Africa"), ("South Korea", "South Korea"), ("Spain", "Spain"), ("Sri Lanka", "Sri Lanka"), ("St Kitts/Nevis", "St Kitts/Nevis"), ("St Vince & The Gs", "St Vince & The Gs"), ("Suriname", "Suriname"), ("Sweden", "Sweden"), ("Switzerland", "Switzerland"), ("Tajikistan", "Tajikistan"), ("Tanzania", "Tanzania"), ("Thailand", "Thailand"), ("Togo", "Togo"), ("Trinidad & Tobago", "Trinidad & Tobago"), ("Tunisia", "Tunisia"), ("Turkmenistan", "Turkmenistan"), ("Uae", "Uae"), ("Uganda", "Uganda"), ("Ukraine", "Ukraine"), ("United Kingdom", "United Kingdom"), ("United States", "United States"), ("Uruguay", "Uruguay"), ("Uzbekistan", "Uzbekistan"), ("Vietnam", "Vietnam"), ("Zambia", "Zambia"), ("Zimbabwe", "Zimbabwe")
)

USER_TYPE_CHOICES = ( 
    ("Admin", "Admin"),
     ("Regular", "Regular"),
      ("Visitor", "Visitor"),
    
)

ATTACHMENT_TYPE_OPTIONS = (
  ('Image', 'Image'),
  ('Video', 'Video'),
)
    
class UserManager(BaseUserManager):
    """Define a model manager for User model with no username field."""

    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        """Create and save a User with the given email and password."""
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        """Create and save a regular User with the given email and password."""
        extra_fields.setdefault('user_type', 'Buyer')
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        """Create and save a SuperUser with the given email and password."""
        extra_fields.setdefault('user_type', 'Admin')

        if extra_fields.get('user_type') != 'Admin':
            raise ValueError('Superuser must have user_type=Admin.')

        user =  self._create_user(email, password, **extra_fields)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

def current_year():
    return datetime.date.today().year

def max_value_current_year(value):
    return MaxValueValidator(current_year())(value)

class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_group'

class User(AbstractBaseUser,PermissionsMixin):
    """User model."""

    name = models.CharField(max_length=255, null=False, default='Name N/A')
    email = models.EmailField(verbose_name='email address', max_length=255, unique=True)
    phone1 = models.CharField(max_length=255, null=False, default='Name N/A')
    phone2 = models.CharField(max_length=255, null=False, default='Name N/A')
    twitter_handle = models.CharField(max_length=255, null=False, default='Name N/A')
    user_type = models.CharField(max_length=100, choices=USER_TYPE_CHOICES, default='Regular')
    bio=models.TextField(blank=True, default='N/A')
    slug = models.SlugField(null=False,unique=True, editable=False)
    
    administration = models.CharField(max_length=255, null=False, default='')
    active = models.BooleanField(blank=True, null=True)
    action_id = models.IntegerField(blank=True, null=True)
    suspend_user = models.CharField(max_length=200, blank=True, null=True)
    permission_hierarchy = models.CharField(max_length=200, blank=True, null=True)
    region = models.CharField(max_length=200, blank=True, null=True)
    business_unit = models.CharField(max_length=200, blank=True, null=True)
    service_center = models.CharField(max_length=200, blank=True, null=True)
    can_approve = models.BooleanField(blank=True, null=True,default=False)
    bucode = models.CharField(max_length=200, blank=True, null=True)
    enable_2fa = models.BooleanField(blank=True, null=True,default=False)
    secret_code_2fa = models.CharField(max_length=200, blank=True, null=True)
    can_manage_2fa = models.BooleanField(blank=True, null=True,default=False)
    position = models.CharField(max_length=200, blank=True, null=True)
    can_approve_caad = models.BooleanField(blank=True, null=True,default=False)
    can_create_user = models.BooleanField(blank=True, null=True,default=False)
    can_create_customer = models.BooleanField(blank=True, null=True,default=False)
    is_dev = models.BooleanField(blank=False, null=True,default=False)
    
    # groups = models.ManyToManyField(AuthGroup)
    
    avatar = models.FileField(upload_to='user_avatar', null=True, blank=True)
    otp = models.IntegerField(blank=True, validators=[MinValueValidator(100000), MaxValueValidator(999999)], default=None, null=True)
    otp_expires_at = models.DateTimeField(default= timezone.now)
        
    is_verified_account = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=True)
    is_regularuser = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)
    created_at = models.DateTimeField(default= timezone.now)
    last_login = models.DateTimeField(null=True,blank=True)
    updated_at = models.DateTimeField(default= timezone.now)
    
    enable_2fa = models.BooleanField(
        verbose_name="Two Factor Authentication",
        default=False,
    )
    secret_code_2fa = models.CharField(
        verbose_name="Two Factor Authentication Secret Code",
        max_length=255,
        blank=True,
        null=True,
    )
    qr_image_2fa = models.BinaryField(
        verbose_name="Two Factor Authentication QR Code",
        blank=True,
        null=True,
    )

    objects = UserManager()

    USERNAME_FIELD = 'email'
    
    def create_user(data):
        user = User.objects.create_user(username=data.username, email=data.email, password=data.password)
        

    # def save(self, *args, **kwargs):
    #     """
    #     Overload core method to check access rights for changing 2FA.
    #     If `enable_2fa` in `vals` check access for action
    #     via `_can_change_2f_auth_settings`.
    #     """
    #     if "enable_2fa" in self.changed_fields:
    #         self._can_change_2f_auth_settings(self)

    #     super(User, self).save(*args, **kwargs)

    def _inverse_enable_2fa(self):
        """
        Inverse `enable_2fa` - call `action_discard_2f_auth_credentials` method
        if value of the field become `false`
        """
        if not self.enable_2fa:
            self.action_discard_2f_auth_credentials()
    
    def action_discard_2f_auth_credentials(self):
        """
        Remove values from fields `qr_image_2fa`, `auth_secret_code_2fa`.
        This method calling when value of the field `enable_2fa` become `false`.
        Field `enable_2fa` can be changed only after checking rights for this action
        in method `write` and no need to check rights for
        `action_discard_2f_auth_credentials`.
        """
        values = {
            "qr_image_2fa": False,
            "secret_code_2fa": False,
        }
        self.write(values)

    def action_disable_2f_auth(self):
        """
        Set `enable_2fa` field value to `False`.
        """
        values = {
            "enable_2fa": False,
        }
        self.write(values)

    def action_enable_2f_auth(self):
        """
        Set `enable_2fa` field value to `False`.
        """
        values = {
            "enable_2fa": True,
        }
        self.write(values)

    def _check_credentials(self, password,kw):
        """
        Overload core method to also check Two Factor Authentication credentials.
        Raises:
         * odoo.addons.two_factor_otp_auth.exceptions.MissingOtpError - no
            `otp_code` in request params. Should be caught by controller and
            render and open enter "one-time-password" page or QR code creation
        """
        print("\n\n\n\n\nPassword from screen ",password,request.params, kw)
        super(User, self)._check_credentials(password,kw)
        # self.enable_2fa=True
        # print("TWO FA?? ",self.enable_2fa)
        if self.enable_2fa:
            params = request.params
            print("params", params)
            secret_code = self.secret_code_2fa or params.get("secret_code_2fa")
            if params.get("otp_code") is None:
                request.session.otk_uid = self.id
                raise MissingOtpError()
            else:
                # can trigger `InvalidOtpError`
                self._check_otp_code(
                    params.pop("otp_code"),
                    secret_code,
                )
            
    def _generate_secrets(self):
        """
        Generate QR-Code based on random set of letters
        Returns:
         * tuple - generated secret_code and binary qr-code
        """
        self.ensure_one()
        key = b32encode(urandom(10))
        code = pyotp.totp.TOTP(key).provisioning_uri(self.login)
        img = qrcode.make(code)
        _, file_path = mkstemp()  # creating temporary file
        img.save(file_path)

        with open(file_path, "rb") as image_file:
            qr_image_code = b64encode(image_file.read())

        # removing temporary file
        with suppress(OSError):
            remove(file_path)

        return key, qr_image_code

    @staticmethod
    def _can_change_2f_auth_settings(user):
        """
        Checking that user can make mass actions with 2FA settings.
        Argument:
        * user - `res.users` object
        Raises:
         * odoo.exceptions.AccessError: only users with `Mass Change 2FA Configuration
          for Users` rights can do this action
        """
        if not user.has_group("two_factor_otp_auth.mass_change_2fa_for_users"):
            raise AccessError(_(
                "Only users with 'Mass Change 2FA Configuration "
                "for Users' rights can do this operation!"
            ))

    @staticmethod
    def _check_otp_code(otp, secret):
        """
        Validate incoming one time password `otp` witch secret via `pyotp`
        library methods.
        Args:
         * otp(str/integer) - one time password
         * secret(str) - origin secret of QR Code for one time password
           generator
        Raises:
         * odoo.addons.two_factor_otp_auth.exceptions.InvalidOtpError -
            one-time-password. Should be caught by controller and return user
            to enter "one-time-password" page
        Returns:
         * bool - True
        """
        print("Frontend otp & secret ",otp, secret)
        totp = pyotp.TOTP(secret)
        print("Totp ", totp)
        str_otp = str(otp)
        print("String otp ",str_otp)
        verify = totp.verify(str_otp)
        if not verify:
            raise InvalidOtpError()
        return True


    def is_admin(self):
        return self.user_type == 'Admin'
    
    def generate_slug(self):
        value = self.name + '-'+  self.email
        slug_candidate = slug_original = slugify(value, allow_unicode=True)
        for i in itertools.count(1):
            if not User.objects.filter(slug=slug_candidate).exists():
                break
            slug_candidate = '{}-{}'.format(slug_original, i)

        self.slug = slug_candidate

    def save(self, *args, **kwargs):
        if not self.pk:
            self.generate_slug()
        super().save(*args, **kwargs)
    
    def is_level_user(self, level):
        return self.permission_hierarchy == level


class UserPreferences(models.Model):
    user = models.ForeignKey(User, models.DO_NOTHING, related_name="user", blank=True, null=True)
    billing_main_page = models.CharField(max_length=1000, blank=True, null=True)
    payments_main_page = models.CharField(max_length=1000, blank=True, null=True)
    personal_info_page = models.CharField(max_length=1000, blank=True, null=True)
    cust_billing_page = models.CharField(max_length=1000, blank=True, null=True)
    cust_payment_page = models.CharField(max_length=1000, blank=True, null=True)
    cust_metering_page = models.CharField(max_length=1000, blank=True, null=True)
    cust_assets_page = models.CharField(max_length=1000, blank=True, null=True)
    create_uid = models.ForeignKey(User, models.DO_NOTHING, db_column='create_uid', blank=True, null=True)
    create_date = models.DateTimeField(blank=True, null=True)
    write_uid = models.ForeignKey(User, models.DO_NOTHING, related_name="users_pref_updated", db_column='write_uid', blank=True, null=True)
    write_date = models.DateTimeField(blank=True, null=True)
    customerstransientviews = models.CharField(max_length=1000, blank=True, null=True)

    # class Meta:
    #     managed = False
    #     db_table = 'user_preferences'
    
class UserJWTtokens(models.Model):
    user_id = models.IntegerField()
    token = models.CharField(max_length=255)
    createdAt = models.DateTimeField(auto_now_add=True)
    expiredAt = models.DateTimeField()
    
class UsersLog(models.Model):
    create_uid = models.ForeignKey(User, models.DO_NOTHING, db_column='create_uid', blank=True, null=True)
    create_date = models.DateTimeField(blank=True, null=True)
    write_uid = models.ForeignKey(User, models.DO_NOTHING, related_name="users_log_update", db_column='write_uid', blank=True, null=True)
    write_date = models.DateTimeField(blank=True, null=True)

    # class Meta:
    #     managed = False
    #     db_table = 'res_users_log'
        
class UserPositions(models.Model):
    name = models.CharField(unique=True, max_length=200, blank=True, null=True)
    code = models.CharField(unique=True, max_length=200, blank=True, null=True)
    position_code = models.CharField(max_length=200, blank=True, null=True)
    create_uid = models.ForeignKey(User, models.DO_NOTHING, db_column='create_uid', blank=True, null=True)
    create_date = models.DateTimeField(blank=True, null=True)
    write_uid = models.ForeignKey(User, models.DO_NOTHING, related_name="users_pos_update", db_column='write_uid', blank=True, null=True)
    write_date = models.DateTimeField(blank=True, null=True)

    # class Meta:
    #     managed = False
    #     db_table = 'user_positions'
        

class UserprocessHierarchy(models.Model):
    process_code = models.CharField(max_length=30, blank=True, null=True)
    position_code = models.CharField(max_length=30, blank=True, null=True)
    create_uid = models.ForeignKey(User, models.DO_NOTHING,related_name='cuph', db_column='create_uid', blank=True, null=True)
    create_date = models.DateTimeField(blank=True, null=True)
    write_uid = models.ForeignKey(User, models.DO_NOTHING, related_name='updateuph', db_column='write_uid', blank=True, null=True)
    write_date = models.DateTimeField(blank=True, null=True)
    precedence = models.IntegerField(blank=True, null=True)


    # class Meta:
    #     managed = False
    #     db_table = 'userprocess_hierarchy'
    
class ResetPassword(models.Model):
    email = models.CharField(max_length=255)
    otp = models.CharField(max_length=255, blank=True, null=True)
    reset_password_token = models.CharField(max_length=255, unique=True)
    otp_expires_at = models.DateTimeField(default='2000-01-01 01:01:30.475275')
    
def get_processes():
    """Process codes"""
    
    processes = [   {"code":"CUST-CU","name":"Customer Creation/Update Process"},
                    {"code":"CUST-KYC","name":"Customer Kyc Approval Process"},
                    {"code":"BHM-OPC","name":"BHM & Operations Compliance"},
                    {"code":"CAAD","name":"Customer Account Adjustment Document"},
                ]
    return processes
