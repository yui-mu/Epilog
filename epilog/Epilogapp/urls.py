from django.urls import path
from django.contrib.auth import views as auth_views

from .views import register_view

urlpatterns = [
    path('register/', register_view, name='register'),
     path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
]
