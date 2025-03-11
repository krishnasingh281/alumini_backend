from rest_framework import serializers
from .models import AlumniProfile

class AlumniProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = AlumniProfile
        fields = '__all__'  # Include all fields
