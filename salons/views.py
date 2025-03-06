from django.shortcuts import render
from rest_framework import viewsets
from .models import Salon, Service, Employee, SalonCustomer, EmployeeWorkingHours
from .serializers import (
    SalonSerializer, 
    ServiceSerializer, 
    EmployeeSerializer, 
    SalonCustomerSerializer, 
    EmployeeWorkingHoursSerializer, 
    EmployeeWorkingHoursUpdateSerializer,
    EmployeeDaysOffSerializer
)
from commons.base_api_viewset import BaseApiViewSet
from django_filters import rest_framework as filters
from rest_framework.decorators import action
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
        
    def retrieve(self, request, *args, **kwargs):
        try:
            queryset = self.get_queryset().get(id=kwargs['pk'])
            serializer = self.get_serializer(queryset)
            return self.success_response('Service fetched successfully', serializer.data)
        except Exception as e:
            return self.error_response(str(e))
    
    def create(self, request):
        try:
            serializer = self.get_serializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return self.success_response('Service created successfully', serializer.data)
            return self.error_response(serializer.errors)
        except Exception as e:
            return self.error_response(str(e))
        
    def update(self, request, *args, **kwargs):
        try:
            return super().update(request, *args, **kwargs) 
        except Exception as e:
            return self.error_response(str(e))
        
    def destroy(self, request, *args, **kwargs):
        try:
            return super().destroy(request, *args, **kwargs)
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
    

class SalonCustomerFilter(filters.FilterSet):
    salon_id = filters.NumberFilter(field_name='salon_id', lookup_expr='exact', required=True)
    full_name = filters.CharFilter(field_name='full_name', lookup_expr='icontains')

    class Meta:
        model = SalonCustomer
        fields = ['salon_id']



class SalonCustomerViewSet(BaseApiViewSet):
    queryset = SalonCustomer.objects.all()
    serializer_class = SalonCustomerSerializer
    filter_backends = [filters.DjangoFilterBackend]
    filterset_class = SalonCustomerFilter
    

    def list(self, request):
        try:
            queryset = self.filter_queryset(self.get_queryset())
            serializer = self.get_serializer(queryset, many=True)   
            return self.success_response('Salon customers fetched successfully', serializer.data)
        except Exception as e:
            return self.error_response(str(e))
    
    def retrieve(self, request, *args, **kwargs):
        try:
            queryset = self.filter_queryset(self.get_queryset())
            customer = queryset.get(id=kwargs['pk'])
            serializer = self.get_serializer(customer)
            return self.success_response('Salon customer fetched successfully', serializer.data)
        except Exception as e:
            return self.error_response(str(e))

    def create(self, request):
        try:
            serializer = self.get_serializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return self.success_response('Salon customer created successfully', serializer.data)
            return self.error_response(serializer.errors)
        except Exception as e:
            return self.error_response(str(e))
    
    def update(self, request, *args, **kwargs):
        try:
            instance = self.get_queryset().get(id=kwargs['pk'])
            serializer = self.get_serializer(instance, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return self.success_response('Salon customer updated successfully', serializer.data)
            return self.error_response(serializer.errors)
        except Exception as e:
            return self.error_response(str(e))
    
    def destroy(self, request, *args, **kwargs):
        try:
            # delete the customer and the user
            customer = self.get_queryset().get(id=kwargs['pk'])
            customer.user.delete()
            customer.delete()
            return self.success_response('Salon customer deleted successfully')
        except Exception as e:
            return self.error_response(str(e))

class EmployeeFilter(filters.FilterSet):
    salon_id = filters.NumberFilter(field_name='salon_id', lookup_expr='exact', required=False)

    class Meta:
        model = Employee
        fields = ['salon_id']

class SalonEmployeeViewSet(BaseApiViewSet):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
    filter_backends = [filters.DjangoFilterBackend]
    filterset_class = EmployeeFilter

    def list(self, request):
        try:
            queryset = self.filter_queryset(self.get_queryset())
            serializer = self.get_serializer(queryset, many=True)
            return self.success_response('Employees fetched successfully', serializer.data)
        except Exception as e:
            return self.error_response(str(e))
        
    def retrieve(self, request, *args, **kwargs):
        try:
            queryset = self.filter_queryset(self.get_queryset())
            employee = queryset.get(id=kwargs['pk'])
            serializer = self.get_serializer(employee)
            return self.success_response('Employee fetched successfully', serializer.data)
        except Exception as e:
            return self.error_response(str(e))
        
    def create(self, request):
        try:
            serializer = self.get_serializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return self.success_response('Employee created successfully', serializer.data)
            return self.error_response(serializer.errors)
        except Exception as e:
            return self.error_response(str(e))
        
    def update(self, request, *args, **kwargs):
        try:
            return super().update(request, *args, **kwargs)
        except Exception as e:
            return self.error_response(str(e))
        
    def destroy(self, request, *args, **kwargs):
        try:
            return super().destroy(request, *args, **kwargs)
        except Exception as e:
            return self.error_response(str(e))

    @action(
            detail=False, 
            methods=['get'],
            url_path='working-hours'
    )
    def get_employee_working_hours(self, request, *args, **kwargs):
        try:
            employee_id = request.query_params.get('employee_id')
            queryset = EmployeeWorkingHours.objects.filter(employee_id=employee_id)
            serializer = EmployeeWorkingHoursSerializer(queryset, many=True)
            if not employee_id:
                return self.error_response('Employee ID is required')
            employee = self.get_queryset().get(id=employee_id)
            return self.success_response('Employee working hours fetched successfully', serializer.data)    
        except Exception as e:
            return self.error_response(str(e))

    @action(
            detail=False,
            methods=['put'],
            url_path='update-working-hours'
    )
    def update_employee_working_hours(self, request, *args, **kwargs):
        try:
            print("update_employee_working_hours:: ", request.data)
            employee_id = request.query_params.get('employee_id')
            if not employee_id:
                return self.error_response('Employee ID is required')
            
            working_hours_data = request.data
            if not isinstance(working_hours_data, list):
                return self.error_response('Expected a list of working hours')

            updated_records = []
            for day_data in working_hours_data:
                working_hours, created = EmployeeWorkingHours.objects.update_or_create(
                    employee_id=employee_id,
                    day=day_data.get('day'),
                    defaults={
                        'start_time': day_data.get('start_time'),
                        'end_time': day_data.get('end_time'),
                        'is_day_off': day_data.get('is_day_off', False),
                        'is_active': day_data.get('is_active', True)
                    }
                )
                updated_records.append(working_hours)
            
            serializer = EmployeeWorkingHoursSerializer(updated_records, many=True)
            print("serializer:: ", serializer.data)
            return self.success_response('Employee working hours updated successfully', serializer.data)
        except Exception as e:
            print("error:: ", e)
            return self.error_response(str(e))