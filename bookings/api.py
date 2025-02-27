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
    r'', 
    views.BookingViewSet, 
    basename='bookings',
)

