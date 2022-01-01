from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.core.validators import RegexValidator
from django.db import models
from django.utils import timezone

from django.contrib.auth.models import UserManager


class CustomUserManager(UserManager):

    def _create_user(self, username, phone_number, password, **extra_fields):
        if not username:
            raise ValueError('The given username must be set')
        user = self.model(username=username, phone_number=phone_number, **extra_fields)
        user.password = make_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, username, phone_number=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(username, phone_number, password, **extra_fields)

    def create_superuser(self, username, phone_number=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(username, phone_number, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    """
    This User model inherits from the Django AbstractBaseUser
    It's the default User model of this project
    """
    username_validator = UnicodeUsernameValidator()
    username = models.CharField(
        'username',
        max_length=150,
        unique=True,
        help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.',
        validators=[username_validator],
        error_messages={
            'unique': "A user with that username already exists.",
        },
    )
    phone_number = models.CharField(max_length=11, validators=[RegexValidator(regex=r"09\d{9}")], unique=True)
    is_staff = models.BooleanField(
        'staff status',
        default=False,
        help_text='Designates whether the user can log into this admin site.',
    )
    is_active = models.BooleanField(
        'active',
        default=True,
        help_text=
        'Designates whether this user should be treated as active. '
        'Unselect this instead of deleting accounts.'
        ,
    )
    date_joined = models.DateTimeField('date joined', default=timezone.now)

    objects = CustomUserManager()
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['phone_number']
