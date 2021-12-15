from django.urls import path
from . import views

urlpatterns = [
    path("login/", views.loginUser, name="login"),
    path("register/", views.registerUser, name="register"),
    path("logout/", views.logoutUser, name="logout"),
    path("", views.profiles, name="profiles"),
    path("profile/<str:pk>", views.userProfile, name="user-profile"),
    path("account/", views.userAccount, name="account"),
    path("edit-account/", views.editAccount, name="edit-account"),
    path("create-skill", views.createSkill, name="create-skill"),
    path("update-skill/<str:pk>", views.updateSkill, name="update-skill"),
    path("delete-skill/<str:pk>", views.deleteSkill, name="delete-skill"),
    path("user-inbox/", views.userInbox, name="user-inbox"),
    path("user-message/<str:pk>/", views.viewUserMessage, name="user-message"),
    path("create-message/<str:pk>/", views.createMessage, name="create-message"),

]
