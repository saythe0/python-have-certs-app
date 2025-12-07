from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views. register_view, name='register'),
    path('login/', views. login_view, name='login'),
    path('logout/', views. logout_view, name='logout'),
    path('applications/', views. applications_list, name='applications_list'),
    path('applications/create/', views.application_create, name='application_create'),
    path('applications/<int:pk>/review/', views.review_create, name='review_create'),
]