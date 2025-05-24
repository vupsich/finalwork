from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Users must have an email address')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

class User(AbstractBaseUser):
    GENDER_CHOICES = [
        ('male', 'Мужской'),
        ('female', 'Женский'),
    ]

    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.EmailField(unique=True)
    gender = models.CharField(max_length=6, choices=GENDER_CHOICES)
    birth_date = models.DateField()
    city = models.CharField(max_length=100)
    language = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'gender', 'birth_date', 'city', 'language']
