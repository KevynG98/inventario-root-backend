from django.urls import path
from ..views.usersViews import *

urlpatterns = [
    path('', all_users),
    path('login/', login),
    path('register/', register),
    path('profile/', profile),
    path('recent/', recent_users),
    path('delete/<int:id>/', delete_user),
]