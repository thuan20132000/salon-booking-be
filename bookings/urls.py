from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'bookings', views.BookingViewSet)
router.register(r'booking-services', views.BookingServiceViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
