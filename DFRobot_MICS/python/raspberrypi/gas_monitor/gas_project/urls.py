from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from sensor.views import GasReadingViewSet

router = routers.DefaultRouter()
router.register(r'gas', GasReadingViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
]
#x
