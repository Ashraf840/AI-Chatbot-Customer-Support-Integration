from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from .managers import UserManager   # Manages "Super & Regular Users"
from django.contrib.auth.validators import UnicodeUsernameValidator


username_validator = UnicodeUsernameValidator()

GENDERCHOICES = [
    ('Male', 'Male'),
    ('Female', 'Female'),
    ('Other', 'Other'),
]

class User(AbstractBaseUser, PermissionsMixin):
    # User Info
    email = models.EmailField(verbose_name='Email', max_length=60, unique=True)
    username = models.CharField(
        "username",
        max_length=150,
        unique=True,
        help_text="Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.",
        validators=[username_validator],
        error_messages={
            "unique": "A user with that username already exists!",
        },
    )
    first_name = models.CharField(verbose_name='First Name', max_length=50, blank=True)
    last_name = models.CharField(verbose_name='Last Name', max_length=50, blank=True)
    gender = models.CharField(verbose_name='Gender', max_length=6, choices=GENDERCHOICES, blank=True)
    phone = models.CharField(verbose_name='Primary Contact', max_length=20, blank=True)
    profile_pic = models.ImageField(upload_to='profilePicture', blank=True)
    initial_password = models.CharField(max_length=150, blank=True, null=True)
    is_first_login = models.BooleanField(default=True)
    # Registration, Activity
    date_joined = models.DateField(verbose_name='Date Joined', auto_now_add=True)
    last_login = models.DateTimeField(verbose_name='Last Login', auto_now_add=True)
    last_update = models.DateTimeField(verbose_name="Last Update", auto_now=True)
    # Extend Roles & Permissions
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_cso = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = "User"

    objects = UserManager()

    EMAIL_FIELD = "email"
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    def save(self, *args, **kwargs):
        # TODO: halt save method, create random password, store into "first_time_pass" field, lastly set that random password into the "password" field.
        # TODO: define a field "is_first_login(bool)" to track first-time-login of users.
        # TODO: Hide the two "password" fields while creating new user from dj-admin-panel
        # TODO: make sure to check the password is set only at the user-creation.
        super(User, self).save(*args, **kwargs)
