from django.urls import path
from .views import *

urlpatterns = [
    path('list/prile/<slug:pk>/', TaskProfileListView.as_view(), name='profile_list'),
    path('please_activate/', PleaseActivateView.as_view(), name='please_activate'),
    path('task/sort/<visible>/<finished>/', SortTaskHandlerView.as_view(), name='sort_task'),
    path('task/create/', TaskCreationView.as_view(), name='create_task'),
    path('list/', TaskListView.as_view(), name='list'),
]