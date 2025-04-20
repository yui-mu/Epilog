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
    calendar_events_view,
    record_detail_view,
    product_create_view,
    product_search_view,
    add_favorite_view,
    favorite_list_view,
    remove_favorite_view,
    chat_view,
    chat_user_list_view,
    chat_with_user_view
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
    path('record/<int:pk>/detail/', record_detail_view, name='record_detail'),
    path('product/create/', product_create_view, name='product_create'),
    path('product/search/', product_search_view, name='product_search'),
    path('favorite/add/<int:product_id>/', add_favorite_view, name='add_favorite'),
    path('favorites/', favorite_list_view, name='favorite_list'),
    path('favorite/remove/<int:product_id>/', remove_favorite_view, name='remove_favorite'),
    path('chat/', chat_view, name='chat'),
    path('chat/users/', chat_user_list_view, name='chat_user_list'),
    path('chat/<int:user_id>/', chat_with_user_view, name='chat_with_user'),

    
]
