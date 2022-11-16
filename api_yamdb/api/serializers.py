from rest_framework import serializers
from users.models import User


class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email', 'username']



class VerifySerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'confirmation_code']



 