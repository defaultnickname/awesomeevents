from django.db import models
from django.contrib.auth.models import User, AbstractBaseUser, PermissionsMixin
from django.utils.translation import gettext_lazy as _
from .managers import CustomUserManager

import uuid


class Event(models.Model):
    title = models.CharField(max_length=100)
    thumbnail = models.ImageField(default='/thumbnail-default.jpg', blank=True,upload_to = 'media')
    description = models.TextField(max_length=100)

    start = models.DateField()
    end = models.DateField()

    def __str__(self):
        return f"{self.title} : {self.start} - {self.end}"


class EventUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(_("email address"), unique=True)

    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        if self.is_staff:
            return f"{self.email} - Admin"
        else:
            return f"{self.email} - User"


class Booking(models.Model):
    code = models.CharField(max_length=8, default=uuid.uuid4().hex[:6].upper(), unique=True)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)

    reserved_by = models.ForeignKey(EventUser, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.event.title} reserved by {self.reserved_by}"
