from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import EventViewSet


urlpatterns = [
    path('', EventViewSet.as_view(), name='events'),
]
