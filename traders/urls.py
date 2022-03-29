from django.urls import path

from . import views

urlpatterns = [
   path('login_trader', views.login_trader, name="login"),
   path('logout_trader', views.logout_trader, name="logout"),
   path('register_trader', views.register_trader, name="register")
]