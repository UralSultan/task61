from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView

from .forms import ProjectModelForm, TaskModelForm
from .models import Project, Task


class ProjectListView(ListView):
    model = Project
    template_name = 'taskman/index.html'
    context_object_name = 'projects'
    paginate_by = 5

    def get_queryset(self):
        projects = Project.objects.all()
        query = self.request.GET.get('q')
        if query:
            projects = projects.filter(Q(title__icontains=query) | Q(description__icontains=query))
        return projects

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['q'] = self.request.GET.get('q', '')
        return context


class ProjectDetailView(DetailView):
    model = Project
    template_name = 'taskman/project_detail.html'
    context_object_name = 'project'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tasks'] = self.object.tasks.filter(is_deleted=False)
        return context


class ProjectCreateView(LoginRequiredMixin, CreateView):
    model = Project
    form_class = ProjectModelForm
    template_name = 'taskman/project_create.html'
    success_url = reverse_lazy('taskman:task_list')


class ProjectUpdateView(LoginRequiredMixin, UpdateView):
    model = Project
    form_class = ProjectModelForm
    template_name = 'taskman/project_update.html'

    def get_success_url(self):
        return reverse('taskman:project_detail', kwargs={'pk': self.object.pk})


class ProjectDeleteView(LoginRequiredMixin, DeleteView):
    model = Project
    template_name = 'taskman/project_delete.html'
    success_url = reverse_lazy('taskman:task_list')


class TaskListView(ListView):
    model = Task
    template_name = 'taskman/task_list.html'
    context_object_name = 'tasks'

    def get_queryset(self):
        return Task.objects.filter(is_deleted=False)


class TaskDetailView(DetailView):
    model = Task
    template_name = 'taskman/task_detail.html'
    context_object_name = 'task'

    def get_queryset(self):
        return Task.objects.filter(is_deleted=False)


class TaskCreateView(LoginRequiredMixin, CreateView):
    model = Task
    form_class = TaskModelForm
    template_name = 'taskman/task_create.html'

    def dispatch(self, request, *args, **kwargs):
        self.project = get_object_or_404(Project, pk=kwargs['project_pk']) if 'project_pk' in kwargs else None
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.author = self.request.user
        if self.project:
            form.instance.project = self.project
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['project'] = self.project
        return context

    def get_success_url(self):
        if self.project:
            return reverse('taskman:project_detail', kwargs={'pk': self.project.pk})
        return reverse('taskman:task_list_all')


class TaskUpdateView(LoginRequiredMixin, UpdateView):
    model = Task
    form_class = TaskModelForm
    template_name = 'taskman/task_update.html'

    def get_queryset(self):
        return Task.objects.filter(is_deleted=False)

    def get_success_url(self):
        return reverse('taskman:task_detail', kwargs={'pk': self.object.pk})


class TaskDeleteView(LoginRequiredMixin, DeleteView):
    model = Task
    template_name = 'taskman/task_delete.html'

    def get_queryset(self):
        return Task.objects.filter(is_deleted=False)

    def get_success_url(self):
        if self.object.project_id:
            return reverse('taskman:project_detail', kwargs={'pk': self.object.project_id})
        return reverse('taskman:task_list_all')

    def form_valid(self, form):
        self.object.is_deleted = True
        self.object.save()
        return redirect(self.get_success_url())
