from django.urls import path
from .views import *

urlpatterns = [
    path('list/', TaskListView.as_view(), name='list'),
    path('list/prile/<slug:pk>', TaskProfileListView.as_view(), name='profile_list'),
]