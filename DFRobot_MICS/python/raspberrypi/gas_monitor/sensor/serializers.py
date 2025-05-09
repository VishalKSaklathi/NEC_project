from rest_framework import serializers
from .models import GasReading

class GasReadingSerializer(serializers.ModelSerializer):
    class Meta:
        model = GasReading
        fields = '__all__'
#x
