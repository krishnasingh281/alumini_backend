from django.urls import path
from .views import AlumniProfileView, AlumniListView, export_alumni_pdf

urlpatterns = [
    path('profile/', AlumniProfileView.as_view(), name='alumni-profile'),
    path('list/', AlumniListView.as_view(), name='alumni-list'),
    path("export-alumni-pdf/", export_alumni_pdf, name="export_alumni_pdf"),
]
