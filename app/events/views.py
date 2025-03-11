from rest_framework import viewsets
from rest_framework.permissions import IsAdminUser
from .models import Event
from .serializers import EventsSerializer

class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventsSerializer
    permission_classes = [IsAdminUser]  # Only Admins can CRUD
