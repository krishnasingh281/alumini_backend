from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from alumini.models import AlumniProfile  # Import AlumniProfile

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    role = serializers.ChoiceField(choices=[("alumni", "Alumni"), ("student", "Student")]) 

    class Meta:
        model = User
        fields = ["username", "email", "password", "role", "graduation_year", "current_company"]
        read_only_fields = ('id',)

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True, required=True, validators=[validate_password]
    )
    password2 = serializers.CharField(write_only=True, required=True)
    
    # Add alumni profile fields when needed
    graduation_year = serializers.IntegerField(required=False, write_only=True)
    current_company = serializers.CharField(required=False, write_only=True, allow_blank=True)
    job_title = serializers.CharField(required=False, write_only=True, allow_blank=True)
    bio = serializers.CharField(required=False, write_only=True, allow_blank=True)
    linkedin_url = serializers.URLField(required=False, write_only=True, allow_blank=True)

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password', 'password2', 'role', 
                  'graduation_year', 'current_company', 'job_title', 'bio', 'linkedin_url')
        extra_kwargs = {'email': {'required': True}}

    def validate(self, data):
        """Ensure passwords match and alumni data is present when needed"""
        if data['password'] != data['password2']:
            raise serializers.ValidationError({'password': 'Passwords do not match'})
            
        # If role is alumni, graduation_year is required
        if data.get('role') == 'alumni' and 'graduation_year' not in data:
            raise serializers.ValidationError({'graduation_year': 'Graduation year is required for alumni'})
            
        return data

    def create(self, validated_data):
        validated_data.pop('password2')  # Remove password2
        
        # Extract alumni profile data
        alumni_fields = {}
        for field in ['graduation_year', 'current_company', 'job_title', 'bio', 'linkedin_url']:
            if field in validated_data:
                alumni_fields[field] = validated_data.pop(field)
        
        password = validated_data.pop('password')  # Extract password
        user = User(**validated_data)
        user.set_password(password)  # Hash password properly
        user.save()

        # Create alumni profile if role is alumni
        if user.role == 'alumni':
            try:
                AlumniProfile.objects.create(user=user, **alumni_fields)
                print(f"AlumniProfile created for {user.username} with graduation year: {alumni_fields.get('graduation_year')}")
            except Exception as e:
                print(f"Error creating AlumniProfile: {str(e)}")
                # You might want to delete the user if profile creation fails
                # user.delete()
                # raise serializers.ValidationError({"alumni_profile": str(e)})

        return user
