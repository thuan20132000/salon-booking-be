from rest_framework import serializers
from .models import Salon, Employee, Service, ServiceCategory, SalonCustomer

class SalonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Salon
        fields = [
            'id', 
            'name', 
            'address',
            'phone', 
            'description', 
            'created_at',
        ]
class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = ['id', 'nick_name', 'phone_number', 'role', 'salon', 'is_active', 'is_available']



class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = ['id', 'name', 'description', 'price', 'duration', 'created_at', 'updated_at','salon']


class ServiceCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceCategory
        fields = ['id', 'name', 'description', 'created_at', 'updated_at']


class SalonCustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = SalonCustomer
        fields = [
            'id', 
            'is_active', 
            'created_at', 
            'updated_at',
            'phone_number', 
            'full_name', 
            'address', 
            'email', 
            'birth_date',
            'gender',
            'salon'
        ]
