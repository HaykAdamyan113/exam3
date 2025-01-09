from django.urls import path
from django.contrib.auth import views as auth_views
from . import views


urlpatterns = [
    path('', views.course_list, name='course_list'),  
    path('course/<int:course_id>/', views.course_detail, name='course_detail'),  
    path('rate/<int:course_id>/', views.rate_course, name='rate_course'),  
    path('add/', views.add_course, name='add_course'),  
    path('register/', views.register, name='register'),  
    path('login/', views.login_view, name='login'),  
    path('logout/', views.user_logout, name='logout'),  
]