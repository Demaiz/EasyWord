from django.urls import path
from . import views

app_name = "flashcards"

urlpatterns = [
    path('', views.index, name="index"),
    path('dictionary/', views.dictionary, name="dictionary"),
    path('register/', views.RegisterUser.as_view(), name="register"),
    path('login/', views.LoginUser.as_view(), name="login"),
    path('logout/', views.logout_user, name="logout_user"),
    path('learn/', views.learn, name="learn"),
]
