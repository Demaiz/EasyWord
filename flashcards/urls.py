from django.urls import path
from . import views

app_name = "flashcards"

urlpatterns = [
    path('', views.index, name="index"),
    path('dictionary/', views.dictionary, name="dictionary"),
    path('register/', views.RegisterUser.as_view(), name="register"),
]
