from rest_framework import serializers
from django.contrib.auth.hashers import make_password, check_password
from .models import Admins

class AdminRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = Admins
        fields = ('admin_id', 'admin_email', 'username', 'password')

    def create(self, validated_data):
        password = validated_data.pop('password')
        admin = Admins.objects.create(**validated_data)
        admin.password = make_password(password)
        admin.save()
        return admin

class AdminLoginSerializer(serializers.Serializer):
    admin_email = serializers.EmailField()
    password = serializers.CharField()

    def validate(self, data):
        email = data.get('admin_email')
        password = data.get('password')
        try:
            admin = Admins.objects.get(admin_email=email)
        except Admins.DoesNotExist:
            raise serializers.ValidationError('Invalid credentials')

        if not check_password(password, admin.password):
            raise serializers.ValidationError('Invalid credentials')

        return {
            'admin': admin
        }
