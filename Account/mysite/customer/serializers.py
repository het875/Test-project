from rest_framework import serializers
from .models import *
from django.contrib.auth import get_user_model

class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ('cust_id', 'cust_first_name', 'cust_last_name', 'cust_email', 'cust_phone', 'date_of_birth', 'house_number', 'street_address', 'city', 'state', 'postal_code', 'country')

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    
    class Meta:
        model = Customer
        fields = ('cust_id', 'cust_first_name', 'cust_last_name', 'cust_email', 'cust_phone', 'password', 'date_of_birth', 'house_number', 'street_address', 'city', 'state', 'postal_code', 'country')

    def create(self, validated_data):
        password = validated_data.pop('password')
        customer = Customer.objects.create(**validated_data)
        customer.password = make_password(password)
        customer.save()
        return customer

class LoginSerializer(serializers.Serializer):
    cust_email = serializers.EmailField()
    password = serializers.CharField()

    def validate(self, data):
        email = data.get('cust_email')
        password = data.get('password')
        try:
            customer = Customer.objects.get(cust_email=email)
        except Customer.DoesNotExist:
            raise serializers.ValidationError('Invalid credentials')

        if not customer.is_password_valid(password):
            raise serializers.ValidationError('Invalid credentials')

        return {
            'customer': customer
        }