from rest_framework import serializers

class SignupSerializer(serializers.Serializer):
    First_name = serializers.CharField(max_length=143,required=False)
    Last_name = serializers.CharField(max_length=143,required=False)
    gender = serializers.CharField(max_length=20)
    email = serializers.EmailField(required=True)
    phone_number = serializers.CharField(required=False)

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=143,required=True)
    otp = serializers.CharField(max_length=143,required=True)    