from django.urls import path

from .views import (
    ProjectCreateView,
    ProjectDeleteView,
    ProjectDetailView,
    ProjectListView,
    ProjectUpdateView,
    TaskCreateView,
    TaskDeleteView,
    TaskDetailView,
    TaskListView,
    TaskUpdateView,
    ProjectUsersUpdateView,
)

app_name = "taskman"

urlpatterns = [
    path('', ProjectListView.as_view(), name='task_list'),
    path('tasks/', TaskListView.as_view(), name='task_list_all'),
    path('project/create/', ProjectCreateView.as_view(), name='project_create'),
    path('project/<int:pk>/', ProjectDetailView.as_view(), name='project_detail'),
    path('project/<int:pk>/update/', ProjectUpdateView.as_view(), name='project_update'),
    path('project/<int:pk>/delete/', ProjectDeleteView.as_view(), name='project_delete'),
    path('project/<int:project_pk>/task/create/', TaskCreateView.as_view(), name='task_create'),
    path('task/create/', TaskCreateView.as_view(), name='task_create_without_project'),
    path('task/<int:pk>/', TaskDetailView.as_view(), name='task_detail'),
    path('task/<int:pk>/update/', TaskUpdateView.as_view(), name='task_update'),
    path('task/<int:pk>/delete/', TaskDeleteView.as_view(), name='task_delete'),
    path('project/<int:pk>/users/', ProjectUsersUpdateView.as_view(), name='project_users_update'),
]
