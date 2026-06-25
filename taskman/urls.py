from django.urls import path
from .views import TaskCreateView, TaskUpdateView, IndexView, TaskDetailView, TaskDeleteView

app_name = "taskman"

urlpatterns = [
    path('', IndexView.as_view(), name='task_list'),
    path('task/create/', TaskCreateView.as_view(), name='task_create'),
    path('task/<int:pk>/', TaskDetailView.as_view(), name='task_detail'),
    path('task/<int:pk>/update/', TaskUpdateView.as_view(), name='task_update'),
    path('task/<int:pk>/delete/', TaskDeleteView.as_view(), name='task_delete'),
]
