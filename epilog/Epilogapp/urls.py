from django.urls import path
from django.contrib.auth import views as auth_views
from django.views.generic import TemplateView
from django.contrib.auth.views import (
    PasswordChangeView, 
    PasswordChangeDoneView,
    PasswordResetView,
    PasswordResetDoneView,
    PasswordResetConfirmView,
    PasswordResetCompleteView,      
)
from . import views
from .views import (
    register_view, 
    home_view, top_view, 
    record_create_view, 
    record_list_view, 
    record_edit_view,
    record_detail_view,
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
    chat_with_user_view,
    user_skincare_record_list_view,
    user_record_calendar_view,
    user_record_calendar_events_view,
    profile_view,
    edit_profile_view,
    edit_account_view,
    email_login_view,
    toggle_favorite_ajax,
    CustomPasswordResetView, 
    CustomPasswordResetDoneView,
    
    )



urlpatterns = [
    path('', top_view, name='top'),
    path('register/', register_view, name='register'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('home/', home_view, name='home'),
    path('record/create/', record_create_view, name='record_create'),
    path('record/list/', record_list_view, name='record_list'),
    path('record/edit/<int:pk>/', record_edit_view, name='record_edit'),
    path('record/delete/<int:pk>/', record_detail_view, name='record_delete'),
    path('record/calendar/', calendar_view, name='record_calendar'),
    path('record/calendar/events/', calendar_events_view, name='calendar_events'),
    path('record/<int:pk>/detail/', record_detail_view, name='record_detail'),
    path('record/<int:pk>/edit/', views.record_edit_view, name='record_edit'),
    path('product/create/', product_create_view, name='product_create'),
    path('product/search/', product_search_view, name='product_search'),
    path('favorite/add/<int:product_id>/', add_favorite_view, name='add_favorite'),
    path('favorites/', favorite_list_view, name='favorite_list'),
    path('favorite/remove/<int:product_id>/', remove_favorite_view, name='remove_favorite'),
    path('chat/', chat_view, name='chat'),
    path('chat/users/', chat_user_list_view, name='chat_user_list'),
    path('chat/<int:user_id>/', chat_with_user_view, name='chat_with_user'),
    path('records/user/<int:user_id>/', user_skincare_record_list_view, name='user_skincare_record_list'),
    path('record/user/<int:user_id>/calendar/', user_record_calendar_view, name='user_record_calendar'),
    path('record/user/<int:user_id>/events/', user_record_calendar_events_view, name='user_record_calendar_events'),
    path('password/change/', PasswordChangeView.as_view(template_name='registration/password_change_form.html'), name='password_change'),
    path('password/change/done/', PasswordChangeDoneView.as_view(template_name='registration/password_change_done.html'), name='password_change_done'),
    path('password/reset/', CustomPasswordResetView.as_view(), name='password_reset'),
    path('password/reset/done/', CustomPasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', PasswordResetConfirmView.as_view(
        template_name='registration/password_reset_confirm.html'), name='password_reset_confirm'),
    path('reset/done/', PasswordResetCompleteView.as_view(
        template_name='registration/password_reset_complete.html'), name='password_reset_complete'),
    path('profile/', profile_view, name='profile'),
    path('profile/edit/', edit_profile_view, name='edit_profile'),
    path('account/edit/', edit_account_view, name='edit_account'),
    path('logged_out/', TemplateView.as_view(template_name='registration/logged_out.html'), name='logged_out'),
    path('login/', email_login_view, name='login'),
    path('favorite/ajax/toggle/', toggle_favorite_ajax, name='toggle_favorite_ajax'),
    path('advisor/unassigned/', views.advisor_unassigned_list, name='advisor_unassigned_list'),
    path('advisor/start_chat/<int:session_id>/', views.advisor_start_chat, name='advisor_start_chat'),
    path('advisor/active/', views.advisor_active_chats, name='advisor_active_chats'),
    path('advisor/session/<int:session_id>/', views.chat_session_detail, name='chat_session_detail'),
    path('advisor/session/<int:session_id>/complete/', views.chat_session_complete, name='chat_session_complete'),
    path('advisor/completed/', views.advisor_completed_chats, name='advisor_completed_chats'),
    path('advisor/profile/', views.advisor_profile_view, name='advisor_profile'),



]
