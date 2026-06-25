from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import TemplateView, View
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView
from .models import Task
from .forms import TaskModelForm
from django.contrib.auth.mixins import LoginRequiredMixin


class IndexView(TemplateView):
    template_name = 'taskman/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tasks'] = Task.objects.all()
        return context


class TaskDetailView(TemplateView):
    template_name = 'taskman/task_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['task'] = get_object_or_404(Task, pk=kwargs['pk'])
        return context


class TaskCreateView(LoginRequiredMixin, CreateView):
    model = Task
    form_class = TaskModelForm
    template_name = 'taskman/task_create.html'
    success_url = reverse_lazy('taskman:task_list')

class TaskUpdateView(LoginRequiredMixin, UpdateView):
    model = Task
    form_class = TaskModelForm
    template_name = 'taskman/task_update.html'
    success_url = reverse_lazy('taskman:task_list')


class TaskDeleteView(LoginRequiredMixin, View):
    template_name = 'taskman/task_delete.html'

    def get(self, request, *args, **kwargs):
        task = get_object_or_404(Task, pk=kwargs['pk'])
        return render(request, self.template_name, {'task': task})

    def post(self, request, *args, **kwargs):
        task = get_object_or_404(Task, pk=kwargs['pk'])
        task.delete()
        return redirect('taskman:task_list')


# Create your views here.
