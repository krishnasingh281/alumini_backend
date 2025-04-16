from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from .views import RegisterView, AdminOnlyView, AlumniOnlyView, BulkUploadAlumniView, LoginView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # Protected Routes
    path('admin-only/', AdminOnlyView.as_view(), name='admin-only'),
    path('alumni-only/', AlumniOnlyView.as_view(), name='alumni-only'),
    path("bulk-upload-alumni/", BulkUploadAlumniView.as_view(), name="bulk_upload_alumni"),
]
