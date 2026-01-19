from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('register/', views.register, name='register'),
    path('delete_goal/<int:goal_id>/', views.delete_goal, name='delete_goal'),
]