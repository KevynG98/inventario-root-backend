from django.urls import path
from ..views.usersViews import login, logout, register

urlpatterns = [
    path('login/', login),
    path('register/', register),
    path('logout/', logout, name='logout'),
]
