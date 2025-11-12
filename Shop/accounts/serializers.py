from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from .models import CustomUser
class UserLoginserializer(serializers.Serializer):
    email=serializers.EmailField(required=False,allow_blank=True)
    phone_number=serializers.CharField(required=False,allow_blank=True)
    password=serializers.CharField(write_only=True)
    def validate(self, attrs):
        email = attrs.get('email')
        phone_number = attrs.get('phone_number')
        if not email and not phone_number:
            raise serializers.ValidationError("Either email or phone number must be provided.")
        return super().validate(attrs)