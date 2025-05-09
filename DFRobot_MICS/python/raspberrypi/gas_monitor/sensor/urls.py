#x sensor/urls.py

from django.urls import path
from .views import upload_sensor_data

urlpatterns = [
    path('api/upload', upload_sensor_data, name='upload_sensor_data'),
]
