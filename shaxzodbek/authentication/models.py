import uuid
from datetime import timedelta

from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
    Group,
    Permission,
)
from django.db import models
from django.utils import timezone
from django.urls import reverse
import random


class CustomUserManager(BaseUserManager):
    use_in_migrations = True

    def create_user(self, email, first_name, password=None, **extra_fields):
        if not email:
            raise ValueError("The Email field must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, first_name=first_name, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, first_name, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)
        return self.create_user(email, first_name, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(
        max_length=150, blank=True, null=True, unique=True, default=uuid.uuid4
    )
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150, blank=True, null=True)
    profile_picture = models.ImageField(
        upload_to="profile_pictures/%Y/%M/%d", blank=True, null=True
    )
    slug = models.SlugField(max_length=160, unique=True, default=uuid.uuid4())
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)
    data_of_birth = models.DateField(blank=True, null=True)
    deleted_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name"]

    objects = CustomUserManager()

    @staticmethod
    def generate_otp():
        return "{:06d}".format(random.randint(0, 999999))

    def get_profile_picture(self):
        if self.profile_picture:
            return self.profile_picture.url
        return "https://www.gravatar.com/avatar/"

    def __str__(self):
        return self.email

    def get_absolute_url(self):
        return reverse("user_detail", kwargs={"slug": self.slug})

    @property
    def hash_email(self):
        return self.email[:2] + "*" * len(self.email[2:-11]) + self.email[-11:]


class OneTimePassword(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="otps"
    )  # Changed from OneToOneField to ForeignKey
    passcode = models.CharField(max_length=6)
    purpose = models.CharField(
        max_length=20, default="verification"
    )  # Added purpose field
    created_at = models.DateTimeField(auto_now_add=True)
    expiry = models.DateTimeField(blank=True)  # Remove default value from model

    def __str__(self):
        return f"OTP for {self.user.email}: {self.passcode}"

    def save(self, *args, **kwargs):
        if not self.expiry:
            self.expiry = timezone.now() + timedelta(minutes=5)
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "One Time Password"
        verbose_name_plural = "One Time Passwords"
