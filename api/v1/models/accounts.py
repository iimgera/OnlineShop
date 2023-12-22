from datetime import timedelta
from django.utils import timezone
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import (
    AbstractUser, BaseUserManager, Permission, Group
)


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError(_("The Email must be set"))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError(_("Superuser must have is_staff=True."))
        if extra_fields.get("is_superuser") is not True:
            raise ValueError(_("Superuser must have is_superuser=True."))
        return self.create_user(email, password, **extra_fields)


class User(AbstractUser):
    email = models.EmailField(
        verbose_name='Почта',
        max_length=60, unique=True, blank=True,
        null=True, default='Еще не заполнен'
    )
    username = models.CharField(
        max_length=25, null=True, 
        blank=True, unique=True
    )
    full_name = models.CharField(
        max_length=150, verbose_name='ФИО'
    )
    phone_number = models.CharField(
        max_length=16, verbose_name='Номер телефона',
        unique=True, blank=True, null=True
    )
    groups = models.ManyToManyField(
        Group, related_name='custom_user',
        blank=True
    )
    user_permissions = models.ManyToManyField(
        Permission, related_name='custom_user',
        blank=True
    )
    otp_reset = models.CharField(max_length=6, blank=True, null=True)
    otp_reset_created_at = models.DateTimeField(blank=True, null=True)

    def otp_expired(self):
        if self.otp_reset_created_at:
            expiration_time = self.otp_reset_created_at + timedelta(minutes=5)
            return timezone.now() > expiration_time
        return True

    def save(self, *args, **kwargs):
        if self.otp_reset and not self.otp_reset_created_at:
            self.otp_reset_created_at = timezone.now()
        elif self.otp_reset and self.otp_reset_created_at:
            self.otp_reset_created_at = timezone.now()

        super().save(*args, **kwargs)
    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return f'username:{self.username}, email: {self.email}'

    class Meta:
        app_label = 'accounts'
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
