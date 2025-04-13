from django.urls import path
from django.contrib.auth import views as auth_views
from .views import register_view, home_view, top_view

urlpatterns = [
    path('', top_view, name='top'),
    path('register/', register_view, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('home/', home_view, name='home'),
    
]
