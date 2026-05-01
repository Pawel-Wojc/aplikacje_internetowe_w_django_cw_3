from django.contrib.auth.views import LogoutView
from django.urls import path

from accounts import views
from .views import CustomLoginView, RegisterView, profile_view

urlpatterns = [
    path('login/', CustomLoginView.as_view(), name='login'),
    path('register/', RegisterView.as_view(), name='register'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('profile/', views.profile_view, name='profile'),

]