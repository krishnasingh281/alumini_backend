from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics
from .models import AlumniProfile
from .serializers import AlumniProfileSerializer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters

class AlumniProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """Retrieve the logged-in user's alumni profile"""
        try:
            profile = request.user.alumni_profile  # Fetch profile
            serializer = AlumniProfileSerializer(profile)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except AlumniProfile.DoesNotExist:
            return Response({"error": "Alumni profile not found"}, status=status.HTTP_404_NOT_FOUND)

    def post(self, request):
        """Create or update the alumni profile for the logged-in user"""
        try:
            profile = request.user.alumni_profile  # Check if profile exists
            serializer = AlumniProfileSerializer(profile, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)  # Change status to OK (Update)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except AlumniProfile.DoesNotExist:
            # If no profile exists, create a new one
            serializer = AlumniProfileSerializer(data={**request.data, "user": request.user.id})
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)  # Change status to CREATED
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
class AlumniListView(generics.ListAPIView):
    queryset = AlumniProfile.objects.all()
    serializer_class = AlumniProfileSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]

    # Define filter fields
    filterset_fields = ['current_company', 'job_title', 'graduation_year']
    search_fields = ['user__username', 'current_company', 'job_title', 'bio']
    ordering_fields = ['graduation_year']
    
from django.http import FileResponse
from django.contrib.admin.views.decorators import staff_member_required
from .utils import generate_alumni_pdf  # Import the function

@staff_member_required  # Only admins can access this
def export_alumni_pdf(request):
    """API to export alumni data as a PDF"""
    pdf_buffer = generate_alumni_pdf()
    return FileResponse(pdf_buffer, as_attachment=True, filename="alumni_list.pdf")

