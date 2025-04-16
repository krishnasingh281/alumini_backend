from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from alumini.models import AlumniProfile  # Import AlumniProfile
from django.contrib.auth import authenticate

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    role = serializers.ChoiceField(choices=[("alumni", "Alumni"), ("student", "Student")]) 

    class Meta:
        model = User
        fields = ["username", "email", "password", "role"]
        read_only_fields = ('id',)
        ref_name = 'BlogAppUser'

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True, required=True, validators=[validate_password]
    )
    password2 = serializers.CharField(write_only=True, required=True)
    
    # Only include graduation_year for alumni role validation
    graduation_year = serializers.IntegerField(required=False, write_only=True)

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password', 'password2', 'role', 'graduation_year')
        extra_kwargs = {'email': {'required': True}}

    def validate(self, data):
        """Ensure passwords match and alumni data is present when needed"""
        if data['password'] != data['password2']:
            raise serializers.ValidationError({'password': 'Passwords do not match'})
            
        # If role is alumni, graduation_year is required
        if data.get('role') == 'alumni' and 'graduation_year' not in data:
            raise serializers.ValidationError({'graduation_year': 'Graduation year is required for alumni'})
            
        return data
    
    def validate_graduation_year(self, value):
        import datetime
        current_year = datetime.datetime.now().year
        if value > current_year:
            raise serializers.ValidationError("Graduation year cannot be in the future")
        if value < 1900:
            raise serializers.ValidationError("Please enter a valid graduation year")
        return value

    def create(self, validated_data):
        validated_data.pop('password2')  # Remove password2
        
        # Extract graduation_year for alumni profile
        graduation_year = None
        if 'graduation_year' in validated_data:
            graduation_year = validated_data.pop('graduation_year')  # Remove from data going to User model
        
        password = validated_data.pop('password')  # Extract password
        user = User(**validated_data)  # Create user without graduation_year
        user.set_password(password)  # Hash password properly
        user.save()

        # Create alumni profile if role is alumni
        if user.role == 'alumni' and graduation_year:
            try:
                AlumniProfile.objects.create(user=user, graduation_year=graduation_year)
                print(f"AlumniProfile created for {user.username} with graduation year: {graduation_year}")
            except Exception as e:
                print(f"Error creating AlumniProfile: {str(e)}")

        return user


class LoginSerializer(serializers.Serializer):
    username_or_email = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        """Authenticate user using either username or email"""
        username_or_email = data.get("username_or_email")
        password = data.get("password")

        # Check if user exists with email
        user = User.objects.filter(email=username_or_email).first()
        if user is None:
            # If no user found with email, check by username
            user = User.objects.filter(username=username_or_email).first()

        if user is None:
            raise serializers.ValidationError({"username_or_email": "User not found"})

        # Authenticate user
        user = authenticate(username=user.username, password=password)
        if user is None:
            raise serializers.ValidationError({"password": "Incorrect password"})

        data["user"] = user  # Add the authenticated user to validated data
        return data