from rest_framework import generics
from rest_framework.permissions import IsAdminUser
from .models import Event
from .serializers import EventsSerializer
from .permissions import IsAlumniOrStudent

class EventViewSet(generics.ListAPIView):
    queryset = Event.objects.all()
    serializer_class = EventsSerializer
    
