from django.contrib import admin
from django.urls import path,views

urlpatterns = [
    path('', views.home ,name="home"),
]