from . import views
from django.urls import path


urlpatterns = [
    path('<int:document>/', views.CheckingListCreateView.as_view(), name='check'),
]
