from django.db import models
from django.core import validators
from django.core.validators import RegexValidator
from django.contrib.auth.hashers import make_password, check_password

postal_code_validator = RegexValidator(
    regex=r'^\d{6}$',  # Regex pattern for exactly 6 digits
    message='Postal code must be exactly 6 digits.',
)

class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True, editable=True)
    deleted_at = models.DateTimeField(null=True, blank=True)
    is_blocked = models.BooleanField(default=False)
    is_deleted = models.BooleanField(default=False)

    class Meta:
        abstract = True

class Customer(BaseModel):
    cust_id = models.BigAutoField(primary_key=True)
    cust_first_name = models.CharField(max_length=60)
    cust_last_name = models.CharField(max_length=60)
    cust_email = models.EmailField(unique=True, null=False, blank=False, max_length=55)
    cust_phone = models.CharField(
        null=False, 
        blank=False,
        max_length=15,  
        unique=True,
        validators=[
            validators.RegexValidator(
                regex=r"^\+?91?\d{9,10}$",
                message='Mobile number must be entered in the format: "+999999999". Up to 15 digits allowed.',
            )
        ],
    )
    password = models.CharField(null=False, blank=False, max_length=128)
    date_of_birth = models.DateField(null=True, blank=True)
    house_number = models.CharField(null=False, blank=False, max_length=50)
    street_address = models.CharField(null=False, blank=False, max_length=100)
    city = models.CharField(null=False, blank=False, max_length=50)
    state = models.CharField(null=False, blank=False, max_length=50)
    postal_code = models.CharField(
        null=False, 
        blank=False,
        max_length=6,
        validators=[postal_code_validator],
    )
    country = models.CharField(null=False, blank=False, max_length=50)
    last_login = models.DateTimeField(null=True, blank=True)
    login_status = models.BooleanField(default=False)
    unsuccessful_attempts = models.IntegerField(default=0)
    last_login_attempt = models.DateTimeField(null=True, blank=True)
    is_blocked = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if self.password and not self.password.startswith(('pbkdf2_sha256$', 'bcrypt$', 'argon2$', 'scrypt$')):
            self.password = make_password(self.password)
        super().save(*args, **kwargs)

    def is_password_valid(self, raw_password):
        return check_password(raw_password, self.password)
