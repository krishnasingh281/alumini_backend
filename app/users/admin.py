from django.contrib import admin
from django.urls import path
from django.http import HttpResponseRedirect
from django.utils.html import format_html
from django.shortcuts import render
from django.contrib import messages
from django.contrib.admin.models import LogEntry
import pandas as pd
from django.contrib.auth.admin import UserAdmin
from .models import User
from django.db import connection

class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'role', 'is_staff')
    actions = ['bulk_upload_alumni']

    def bulk_upload_alumni(self, request, queryset):
        """Redirects to bulk upload page."""
        return HttpResponseRedirect("bulk-upload/")
    
    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('bulk-upload/', self.admin_site.admin_view(self.bulk_upload_view), name="bulk-upload-alumni"),
        ]
        return custom_urls + urls
    
    def delete_model(self, request, obj):
        """🔥 Hardcore fix: Force delete logs and user to prevent IntegrityError."""
        with connection.cursor() as cursor:
            cursor.execute("DELETE FROM django_admin_log WHERE user_id = %s", [obj.id])
        obj.delete()
        
        
    def bulk_upload_view(self, request):
        """Handles bulk uploading users from an Excel file."""
        if request.method == "POST":
            excel_file = request.FILES.get("excel_file")

            if not excel_file or not excel_file.name.endswith('.xlsx'):
                messages.error(request, "Invalid file format! Please upload an Excel file (.xlsx).")
                return render(request, "admin/bulk_upload.html")

            try:
                df = pd.read_excel(excel_file)

                for index, row in df.iterrows():
                    user = User.objects.create_user(
                        username=row['username'],
                        email=row['email'],
                        role=row['role']
                    )
                    user.save()

                messages.success(request, "Users uploaded successfully!")
            except Exception as e:
                messages.error(request, f"Error processing file: {e}")

        return render(request, "admin/bulk_upload.html")


# ✅ Unregister User if already registered, then register with CustomUserAdmin
try:
    admin.site.unregister(User)
except admin.sites.NotRegistered:
    pass  # Ignore if it's not registered yet

admin.site.register(User, CustomUserAdmin)
