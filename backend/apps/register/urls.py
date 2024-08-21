from . import views
from django.urls import path


urlpatterns = [
    path('areas/', views.AreaListCreateView.as_view(), name='area-list-create-api'),
    path('areas/<uuid:uuid>/', views.AreaUpdateDeleteView.as_view(), name='area-update-delete-api'),
    path('persons/', views.PersonListCreateView.as_view(), name='person-list-create-api'),
    path('persons/<uuid:uuid>/', views.PersonUpdateDeleteView.as_view(), name='person-update-delete-api'),
]
