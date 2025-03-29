from rest_framework import status, generics
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import RegisterSerializer, UserSerializer
from .models import User
from alumini.models import AlumniProfile

# Register API
class RegisterView(generics.CreateAPIView):
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        
        # No need to create AlumniProfile here - it's handled in the serializer
        
        refresh = RefreshToken.for_user(user)

        return Response({
            'user': UserSerializer(user).data,
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }, status=status.HTTP_201_CREATED)

#  Login API
@api_view(['POST'])
@permission_classes([AllowAny])
def login_view(request):
    username = request.data.get('username')
    password = request.data.get('password')

    if not username or not password:
        return Response({'error': 'Both username and password are required'}, status=status.HTTP_400_BAD_REQUEST)

    user = authenticate(username=username, password=password)

    if user is not None:
        if not user.is_active:
            return Response({'error': 'User account is disabled'}, status=status.HTTP_403_FORBIDDEN)

        refresh = RefreshToken.for_user(user)
        return Response({
            'user': UserSerializer(user).data,
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }, status=status.HTTP_200_OK)

    return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

from rest_framework.permissions import IsAuthenticated
from .permissions import IsAdminUser, IsAlumniUser, IsStudentUser

#  Protect an Admin-only View
class AdminOnlyView(generics.ListAPIView):
    permission_classes = [IsAuthenticated, IsAdminUser]
    queryset = User.objects.all()
    serializer_class = UserSerializer

# Protect an Alumni-only View
class AlumniOnlyView(generics.ListAPIView):
    permission_classes = [IsAuthenticated, IsAlumniUser]
    queryset = User.objects.all()
    serializer_class = UserSerializer
    

import pandas as pd
from rest_framework import status, permissions, views
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from .models import User
from .serializers import UserSerializer

class BulkUploadAlumniView(views.APIView):
    permission_classes = [permissions.IsAdminUser]  # 🚀 Only Admins can use this
    parser_classes = [MultiPartParser, FormParser]  # 🚀 Handle file uploads

    def post(self, request, *args, **kwargs):
        file = request.FILES.get("file")  
        if not file:
            return Response({"error": "No file uploaded"}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            df = pd.read_excel(file)  # 📥 Read Excel file
            required_columns = ["username", "email", "graduation_year", "current_company"]
            
            if not all(col in df.columns for col in required_columns):
                return Response({"error": "Invalid file format. Required columns: username, email, graduation_year, current_company"}, status=status.HTTP_400_BAD_REQUEST)
            
            # 🚀 Process each row and create users
            created_users = []
            for _, row in df.iterrows():
                user_data = {
                    "username": row["username"],
                    "email": row["email"],
                    "role": "alumni",  # Ensure role is set
                    "graduation_year": row["graduation_year"],
                    "current_company": row["current_company"],
                }
                serializer = UserSerializer(data=user_data)
                if serializer.is_valid():
                    serializer.save()
                    created_users.append(serializer.data)
                else:
                    return Response({"error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

            return Response({"message": "Alumni added successfully", "users": created_users}, status=status.HTTP_201_CREATED)
        
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
