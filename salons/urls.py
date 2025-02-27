from django.urls import path, include
from . import views
from .api import router

urlpatterns = [
    path('api/', include(router.urls)),
]
