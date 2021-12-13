from django.urls import path 
from . import views

urlpatterns = [
       path('', views.homePage, name='home'),
       path('project/<str:pk>/', views.projects, name='project'),
       path('create-project', views.createProject, name='create-project'),
       path('update-project/<str:pk>/', views.updateProject, name='update-project'),
       path('delete-project/<str:pk>/', views.deleteProject, name='delete-project'),
]