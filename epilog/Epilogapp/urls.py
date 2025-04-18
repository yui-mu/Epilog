from django.urls import path
from django.contrib.auth import views as auth_views
from .views import (
    register_view, 
    home_view, top_view, 
    record_create_view, 
    record_list_view, 
    record_edit_view,
    record_delete_view,
    calendar_view,
    calendar_events_view
    )



urlpatterns = [
    path('', top_view, name='top'),
    path('register/', register_view, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('home/', home_view, name='home'),
    path('record/create/', record_create_view, name='record_create'),
    path('record/list/', record_list_view, name='record_list'),
    path('record/edit/<int:pk>/', record_edit_view, name='record_edit'),
    path('record/delete/<int:pk>/', record_delete_view, name='record_delete'),
    path('record/calendar/', calendar_view, name='record_calendar'),
    path('record/calendar/events/', calendar_events_view, name='calendar_events'),
    
]
