from rest_framework import viewsets
from .models import GasReading
from .serializers import GasReadingSerializer

class GasReadingViewSet(viewsets.ModelViewSet):
    queryset = GasReading.objects.all()
    serializer_class = GasReadingSerializer
#x
