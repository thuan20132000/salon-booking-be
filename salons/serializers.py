from rest_framework import serializers
from .models import Salon, Employee, Service, ServiceCategory

class SalonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Salon
        fields = ['id', 'name', 'address', 'phone', 'description', 'created_at', 'updated_at']

class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = ['id', 'nick_name', 'phone_number', 'role', 'salon', 'is_active', 'is_available']



class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = ['id', 'name', 'description', 'price', 'duration', 'created_at', 'updated_at']


class ServiceCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceCategory
        fields = ['id', 'name', 'description', 'created_at', 'updated_at']

