from django.urls import path, include
from . import views
from .api import router

urlpatterns = [
    path('api/bookings/', include(router.urls)),
]
