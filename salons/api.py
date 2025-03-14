from . import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(
    r'salons', 
    views.SalonViewSet, 
    basename='salons'
)
router.register(
    r'services', 
    views.ServiceViewSet, 
    basename='services'
)
router.register(
    r'employees', 
    views.EmployeeViewSet, 
    basename='employees',
)
router.register(
    r'salon-customers', 
    views.SalonCustomerViewSet, 
    basename='salon_customers',
)

router.register(
    r'salon-employees', 
    views.SalonEmployeeViewSet, 
    basename='salon_employees',
)

router.register(
    r'customer-booking-history', 
    views.CustomerBookingHistoryViewSet, 
    basename='customer-booking-history'
)

