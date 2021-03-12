from rest_framework import serializers
from datetime import *
from .models import (

    Event,
    EventUser,
    Booking,
)

from django.contrib.auth import authenticate
from .managers import CustomUserManager
from django.utils.translation import ugettext_lazy as _
from django.utils.dateparse import parse_datetime


class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = "__all__"


class EventUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = EventUser
        fields = ("id", "email", "password",)
        extra_kwargs = {
            "password": {"write_only": True},
        }


class BookingAddSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = ("id", "reserved_by", "event")

    def validate(self, data):
        reserved_by = data.get("reserved_by")
        event = data.get("event")

        today = date.today()

        if Booking.objects.filter(reserved_by=reserved_by,event=event).exists():
            raise serializers.ValidationError(_("Already Signed up!"))
        if event.start < today:
            raise serializers.ValidationError(_("Too late to sign for event!"))

        if not event or not reserved_by:
            raise serializers.ValidationError(_("Invalid reservation parameters!"))
        return data


class BookingDeleteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = ("id", "code", "reserved_by", "event")

    def validate(self, data):

        booking = data.get("booking")
        reserved_by = data.get("reserved_by")
        today = date.today()
        event = data.get("event")
        print(today + timedelta(days=2) > event.start)
        print(event.start + timedelta(days=2) < event.end)

        if today + timedelta(days=2) > event.start or event.start + timedelta(days=2) < event.end:
            raise serializers.ValidationError(_("Duration too long, or it is too late to cancel booking!"))

        if not booking or not reserved_by or not event:
            raise serializers.ValidationError(_("Invalid reservation parameters!"))

        return data


class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = EventUser
        fields = ("email", "password")

    def create(self, validated_data):
        return EventUser.objects.create_user(
            email=validated_data["email"], password=validated_data["password"]
        )


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()

    def validate(self, data):
        user = authenticate(**data)

        if user and not user.is_active:
            raise serializers.ValidationError(_("Inactive user"))
        return user
