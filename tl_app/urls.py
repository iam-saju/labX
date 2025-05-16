from django.contrib import admin
from django.urls import path, include
from .views import upload,login,logout

urlpatterns = [
    path('upload/', upload, name='upload'),
    path('',login,name='login'),
    path('logout/', logout, name='logout')
]
