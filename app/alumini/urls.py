from django.urls import path
from .views import AlumniProfileView

urlpatterns = [
    path('profile/', AlumniProfileView.as_view(), name='alumni-profile'),
]
