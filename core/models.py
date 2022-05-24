from itertools import count
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.utils import timezone
from .exceptions import *

# Create your models here.

class UserManager(BaseUserManager):
    def create_user(self, email=None, password=None):
        if not email:
            raise ValueError(_('Users must have an email'))

        user = self.model(
            email=email,
        )

        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password):
        user = self.create_user(
            email=email,
            password=password,
        )

        user.is_admin = True
        user.save(using=self._db)

        return user


class User(AbstractBaseUser):
    USER_TYPE = (('USER', 'USER'), ('ADMIN', 'ADMIN'))
    TYPE_SEX = [('MASCULINO', 'MASCULINO'), ('FEMININO', 'FEMININO'), ('PREFIRO NÃO INFORMAR', 'PREFIRO NÃO INFORMAR')]             
    
    name = models.CharField(max_length=255, blank=False, null=True)
    email = models.EmailField(unique=True, blank=False, null=True)
    phone = models.CharField(max_length=255, blank=True, null=True)
    is_admin = models.BooleanField(default=False)
    active = models.BooleanField(default=True)
    cpf = models.CharField(max_length=50, blank=False, null=True, unique=True)
    type_user = models.CharField(max_length=255, choices=USER_TYPE, default='USER')
    image_user = models.ImageField(upload_to='media', blank=True, null=True)
    cep = models.CharField(max_length=155, blank=True, null=True)
    number = models.CharField(max_length=100, blank=True, null=True)
    street = models.CharField(max_length=255, null=True, blank=True)
    complement = models.CharField(max_length=150, null=True, blank=True)
    neighborhood = models.CharField(max_length=30, null=True, blank=True)
    city = models.CharField(max_length=50, null=True, blank=True)
    state = models.CharField(max_length=50, null=True, blank=True)
    sex = models.CharField(max_length=255, null=True, blank=True,  choices=TYPE_SEX)
    birth_date = models.CharField(max_length=255, null=True, blank=True)
    token_notification = models.CharField(max_length=255, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'

    def get_short_name(self):
        return self.name

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin

    @classmethod
    def change_password(cls, email, forgot_password_hash, new_password):
        try:
            user = cls.objects.get(email=email, forgot_password_hash=forgot_password_hash)
        except cls.DoesNotExist:
            raise ForgotPasswordInvalidParams

        now = timezone.now()

        if user.forgot_password_expire < now:
            raise ForgotPasswordExpired

        user.set_password(new_password)
        user.forgot_password_expire = now
        user.save()

    class Meta:
        ordering = ('-created_at',)         