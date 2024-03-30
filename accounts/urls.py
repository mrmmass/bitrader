from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register_views, name='register'),
    path('api/register', views.register_api , name='register-api'),

    #path('profile/', views.profile, name='profile'),
    path('login/', views.login_views, name='login'),
    path('api/login', views.login_api , name='login-api'),
    path('logout/', views.logout_view, name='logout')
]
