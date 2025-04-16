from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics
from .models import AlumniProfile
from .serializers import AlumniProfileSerializer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from drf_yasg.utils import swagger_auto_schema
from users.permissions import IsAlumniUser
from rest_framework.authentication import SessionAuthentication
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser

class AlumniProfileView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication, SessionAuthentication]
    parser_classes = [MultiPartParser, FormParser, JSONParser]  # Add parsers for handling file uploads

    @swagger_auto_schema(
        operation_description="Retrieve the logged-in user's alumni profile",
        responses={
            200: AlumniProfileSerializer(),
            404: "Alumni profile not found"
        }
    )
    def get(self, request):
        """Retrieve the logged-in user's alumni profile"""
        try:
            profile = AlumniProfile.objects.get(user=request.user)
            serializer = AlumniProfileSerializer(profile)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except AlumniProfile.DoesNotExist:
            return Response({"error": "Alumni profile not found"}, status=status.HTTP_404_NOT_FOUND)

    @swagger_auto_schema(
        operation_description="Create or update the alumni profile for the logged-in user",
        request_body=AlumniProfileSerializer,
        responses={
            200: AlumniProfileSerializer(),
            201: AlumniProfileSerializer(),
            400: "Bad request",
            403: "Not an alumni user"
        }
    )
    def post(self, request):
        """Create or update the alumni profile for the logged-in user"""
        # First, check if the user is actually an alumni
        if request.user.role != 'alumni':
            return Response(
                {"error": "Only alumni users can create/update alumni profiles"}, 
                status=status.HTTP_403_FORBIDDEN
            )
            
        profile = None
        try:
            profile = AlumniProfile.objects.get(user=request.user)
            serializer = AlumniProfileSerializer(
                profile, 
                data=request.data, 
                partial=True,
                context={'request': request}
            )
        except AlumniProfile.DoesNotExist:
            # If no profile exists, create a new one
            serializer = AlumniProfileSerializer(
                data=request.data,
                context={'request': request}
            )
        
        if serializer.is_valid():
            serializer.save(user=request.user)  # Explicitly set the user
            status_code = status.HTTP_200_OK if profile else status.HTTP_201_CREATED
            return Response(serializer.data, status=status_code)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
class AlumniListView(generics.ListAPIView):
    queryset = AlumniProfile.objects.all()
    serializer_class = AlumniProfileSerializer
    authentication_classes = [JWTAuthentication, SessionAuthentication]
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]

    # Define filter fields - now includes department and location
    filterset_fields = ['current_company', 'job_title', 'graduation_year', 'department', 'location']
    search_fields = ['user__username', 'current_company', 'job_title', 'bio', 'department', 'location']
    ordering_fields = ['graduation_year']
    
from django.http import FileResponse
from django.contrib.admin.views.decorators import staff_member_required
from .utils import generate_alumni_pdf  # Import the function

@staff_member_required  # Only admins can access this
def export_alumni_pdf(request):
    """API to export alumni data as a PDF"""
    pdf_buffer = generate_alumni_pdf()
    return FileResponse(pdf_buffer, as_attachment=True, filename="alumni_list.pdf")