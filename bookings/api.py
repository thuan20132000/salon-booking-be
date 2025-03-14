from . import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(
    r'calendar', 
    views.BookingCalendarViewSet, 
    basename='bookings-calendar'
)
router.register(
    r'services', 
    views.BookingServiceViewSet, 
    basename='bookings-services'
)

router.register(
    r'appointments', 
    views.BookingAppointmentsViewSet, 
    basename='booking-appointments'
)

router.register(
    r'employee-appointments', 
    views.EmployeeServiceAppointmentViewSet, 
    basename='employee-appointments'
)


router.register(
    r'employee-booking-availability', 
    views.EmployeeBookingAvailabilityViewSet, 
    basename='employee-booking-availability'
)


router.register(
    r'', 
    views.BookingViewSet, 
    basename='bookings',
)

