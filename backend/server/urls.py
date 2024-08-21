from django.contrib import admin
from django.urls import path, include
from rest_framework import routers

# Api router
router = routers.DefaultRouter()

urlpatterns = [
    # Admin routes only in develop
    path('admin/', admin.site.urls),

    # Api routes
    path('api/checking/', include('apps.checking.urls')),
    path('api/register/', include('apps.register.urls')),
    path('api/auth/', include('apps.authentication.urls')),
    path('api/', include(router.urls)),
]
