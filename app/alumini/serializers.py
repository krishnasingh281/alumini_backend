from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import AlumniProfile

User = get_user_model()

class UserBasicSerializer(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField()
    
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'full_name']
        
    def get_full_name(self, obj):
        return f"{obj.first_name} {obj.last_name}" if hasattr(obj, 'first_name') else obj.username

class AlumniProfileSerializer(serializers.ModelSerializer):
    user_details = UserBasicSerializer(source='user', read_only=True)
    
    class Meta:
        model = AlumniProfile
        fields = [
            'id', 'user', 'user_details', 'graduation_year', 
            'current_company', 'job_title', 'bio', 
            'linkedin_url', 'profile_picture'
        ]
        extra_kwargs = {
            'user': {'write_only': True, 'required': False},  # Hide user ID in responses
            'profile_picture': {'required': False}
        }
        
    def validate(self, data):
        # Ensure users can only modify their own profiles
        request = self.context.get('request')
        if request and hasattr(request, 'user'):
            if 'user' in data and data['user'] != request.user:
                raise serializers.ValidationError("You can only update your own profile")
        return data