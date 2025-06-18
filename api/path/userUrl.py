from django.urls import path
from ..views.usersViews import *

urlpatterns = [
    path('', all_users),
    path('filter-users/', all_users_filted),
    path('doctor-users/', all_doctor_users),
    path('login/', login),
    path('register/', register),
    path('profile/', profile),
    path('recent/', recent_users),
    path('delete/<int:id>/', delete_user),
    path('update/<int:id>/', update_user),
    path('search/', search_users),
    path('admin-reset-password/<int:id>/', admin_reset_password),
    path('logout/', logout, name='logout'),
    path('<int:id>/', user_detail),
]