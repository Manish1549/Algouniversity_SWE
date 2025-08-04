from django.urls import path, include
from account.views import registration, login_user,logout_user
urlpatterns = [
    path('login/',login_user,name = "login-user"),
    path('register/',registration,name = "registration-user"),
    path('logout/',logout_user,name = "logout-user"),
]