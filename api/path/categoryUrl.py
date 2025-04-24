from django.urls import path
from ..views.categoryViews import *

urlpatterns = [
    path('', list_categories, name='list_categories'),
    path('create/', create_category, name='create_category'),
    path('<int:pk>/', retrieve_category, name='retrieve_category'),
    path('<int:pk>/update/', update_category, name='update_category'),
    path('delete/<int:pk>/', delete_category, name='delete_user'),
]
