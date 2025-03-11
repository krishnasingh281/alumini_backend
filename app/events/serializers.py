from rest_framework import serializers
from .models import Event

class EventsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = '__all__'
        read_only_fields = ('id',)
        
    