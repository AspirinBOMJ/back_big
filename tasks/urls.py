from django.urls import path
from .views import *

urlpatterns = [
    path('list/prile/<slug:pk>/', TaskProfileListView.as_view(), name='profile_list'),
    path('please_activate/', PleaseActivateView.as_view(), name='please_activate'),
    path('task/sort/<profile>/<finished>/', SortTaskHandlerView.as_view(), name='sort_task'),
    path('task/create/', TaskCreationView.as_view(), name='task_create'),
    path('task/delete/<slug:slug>/', TaskDeleteView.as_view(), name='task_delete'),
    path('task/detail/<slug:slug>/', TaskDetailView.as_view(), name='task_detail'),
    path('task/update/<slug:slug>/', TaskUpdateView.as_view(), name='task_update'),
    path('subtask/create/<slug:slug>/', SubTaskCreateView.as_view(), name='subtask_create'),
    path('subtask/activate/<pk>/', SubTaskActivateView.as_view(), name='subtask_activate'),
    path('subtask/delete/<pk>/', SubTaskDeleteView.as_view(), name='subtask_delete'),
    path('comment/create/<slug:slug>/', CommentCreateView.as_view(), name='comment_create'),
    path('comment/delete/<pk>/', CommentDeleteView.as_view(), name='comment_delete'),
    path('list/', TaskListView.as_view(), name='list'),
     path('', HomeView.as_view(), name='home'),
]