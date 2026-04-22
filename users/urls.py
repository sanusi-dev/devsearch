from django.urls import path
from .views import *


urlpatterns = [
    path('login/', login_view, name='login'),
    path('signup/', signup_view, name='signup'),
    path('', logout_user, name='logout_user'),

    path('account/', user_account, name='account'),
    path('profiles/', profile_list, name='profile_list'),
    path('profile/<str:pk>/', profile_detail, name='profile_detail'),
    path('profile_edit/', profile_edit, name='profile_edit'),

    path('inbox/', inbox, name='inbox'),
    path('message/<str:pk>', message, name='message'),
    path('send_message/to/<str:pk>', send_message, name='send_message'),

    path('create_skill/', skill_form, name='create_skill'),
    path('update_skill/<str:pk>/', skill_form, name='update_skill'),
    path('delete_skill/<str:pk>/', delete_skill, name='delete_skill'),

]
