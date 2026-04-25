from django.urls import path

from .views import (
    login_view,
    signup_view,
    logout_user,
    user_account,
    profile_list,
    profile_detail,
    profile_edit,
    inbox,
    message,
    send_message,
    delete_message,
    skill_form,
    delete_skill,
    unsubscribe,
)


urlpatterns = [
    path("login/", login_view, name="login"),
    path("signup/", signup_view, name="signup"),
    path("logout/", logout_user, name="logout_user"),

    path("account/", user_account, name="account"),
    path("", profile_list, name="profile_list"),
    path("profile/<str:pk>/", profile_detail, name="profile_detail"),
    path("profile-edit/", profile_edit, name="profile_edit"),

    path("inbox/", inbox, name="inbox"),
    path("message/<str:pk>/", message, name="message"),
    path("send-message/<str:pk>/", send_message, name="send_message"),
    path("delete-message/<str:pk>/", delete_message, name="delete_message"),

    path("create-skill/", skill_form, name="create_skill"),
    path("update-skill/<str:pk>/", skill_form, name="update_skill"),
    path("delete-skill/<str:pk>/", delete_skill, name="delete_skill"),

    path("unsubscribe/<str:signature>/", unsubscribe, name="unsubscribe"),
]
