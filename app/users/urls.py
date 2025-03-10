from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from .views import RegisterView, login_view, AdminOnlyView, AlumniOnlyView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', login_view, name='login'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # Protected Routes
    path('admin-only/', AdminOnlyView.as_view(), name='admin-only'),
    path('alumni-only/', AlumniOnlyView.as_view(), name='alumni-only'),
]
