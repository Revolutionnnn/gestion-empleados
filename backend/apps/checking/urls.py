from . import views
from django.urls import path


urlpatterns = [
    path('', views.CheckAPIView.as_view(), name='checking-api'),
]
