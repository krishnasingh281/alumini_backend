from django.urls import path
from .views import AlumniProfileView, AlumniListView

urlpatterns = [
    path('profile/', AlumniProfileView.as_view(), name='alumni-profile'),
    path('list/', AlumniListView.as_view(), name='alumni-list'),
]
