from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.LoginView.as_view(), name='auth_login'),
    path('logout/', views.LogoutView.as_view(), name='auth_logout'),
    path('groups/', views.GroupListAPIView.as_view(), name='groups'),
    path('profile/', views.UserProfileView.as_view(), name='user-profile'),
    path('users/', views.UserListCreateAPIView.as_view(), name='users'),
    path('users/<uuid:uuid>/', views.UserDestroyUpdateAPIView.as_view(), name='users'),
    path('send-email/', views.SendEmailView.as_view(), name='send-email'),
]
