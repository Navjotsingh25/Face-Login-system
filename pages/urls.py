from django.contrib import admin
from django.urls import path
from . import views
urlpatterns = [
    
    path('',views.home ,name='home'),
    path('signup/',views.signup_view ,name= 'signup'),
    path('login/',views.login_view ,name= 'login'),
    path('profile/',views.profile_view ,name= 'profile'),
    path('logout/',views.logout_view ,name= 'logout'),
    path('about/',views.about_view ,name= 'about'),
    
]
