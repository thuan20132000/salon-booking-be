from django.shortcuts import render
from rest_framework import viewsets
from .models import Salon, Service, Employee, SalonCustomer
from .serializers import SalonSerializer, ServiceSerializer, EmployeeSerializer, SalonCustomerSerializer
from commons.base_api_viewset import BaseApiViewSet
# Create your views here.

class BaseSalonViewSet(viewsets.ModelViewSet):
    queryset = Salon.objects.all()
    serializer_class = SalonSerializer
    


class SalonViewSet(BaseSalonViewSet):
    queryset = Salon.objects.all()
    serializer_class = SalonSerializer

class ServiceViewSet(BaseApiViewSet):
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer
    
    def list(self, request):
        try:
            salon_id = request.query_params.get('salon_id')
            if not salon_id:
                return self.error_response('Salon ID is required')
            queryset = self.get_queryset().filter(salon_id=salon_id)
            serializer = self.get_serializer(queryset, many=True)
            return self.success_response('Services fetched successfully', serializer.data)
        except Exception as e:
            return self.error_response(str(e))

class EmployeeViewSet(BaseApiViewSet):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer

    def list(self, request):
        try:
            print(request.query_params)
            salon_id = request.query_params.get('salon_id')
            if not salon_id:
                return self.error_response('Salon ID is required')
            queryset = self.get_queryset().filter(salon_id=salon_id)
            serializer = self.get_serializer(queryset, many=True)
            return self.success_response('Employees fetched successfully', serializer.data)
        except Exception as e:
            return self.error_response(str(e))
    
class SalonCustomerViewSet(BaseApiViewSet):
    queryset = SalonCustomer.objects.all()
    serializer_class = SalonCustomerSerializer
    
    def list(self, request):
        try:
            salon_id = request.query_params.get('salon_id')
            if not salon_id:
                return self.error_response('Salon ID is required')
            queryset = self.get_queryset().filter(salon_id=salon_id)
            serializer = self.get_serializer(queryset, many=True)   
            return self.success_response('Salon customers fetched successfully', serializer.data)
        except Exception as e:
            return self.error_response(str(e))
    