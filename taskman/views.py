from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView
from .forms import ProjectModelForm, TaskModelForm, ProjectUsersForm
from .models import Project, Task


PROJECT_MANAGER = 'Проектный менеджер'
TEAM_LEAD = 'Тим лид'
DEVELOPER = 'разраб'


def user_has_group(user, group_name):
    return bool(user and user.is_authenticated and user.groups.filter(name__iexact=group_name).exists())


def is_project_manager(user):
    return user_has_group(user, PROJECT_MANAGER)


def is_team_lead(user):
    return user_has_group(user, TEAM_LEAD)


def is_developer(user):
    return user_has_group(user, DEVELOPER)


def is_project_user(user, project):
    return bool(user and user.is_authenticated and project.users.filter(pk=user.pk).exists())


def can_create_project(user):
    return bool(user and user.is_authenticated and (user.is_superuser or is_project_manager(user)))


def can_change_project(user, project):
    return bool(user and user.is_authenticated and (user.is_superuser or (is_project_manager(user) and project.author_id == user.id)))


def can_manage_project_users(user, project):
    if not user or not user.is_authenticated:
        return False
    if user.is_superuser:
        return True
    if is_project_manager(user):
        return project.author_id == user.id
    if is_team_lead(user):
        return is_project_user(user, project)
    return False


def can_create_task(user, project):
    if not user or not user.is_authenticated or project is None:
        return False
    if user.is_superuser:
        return True
    if is_project_manager(user):
        return project.author_id == user.id
    if is_team_lead(user) or is_developer(user):
        return is_project_user(user, project)
    return False


def can_change_task(user, task):
    if not user or not user.is_authenticated:
        return False
    if user.is_superuser:
        return True
    if is_project_manager(user):
        return bool(task.project and task.project.author_id == user.id)
    if is_team_lead(user):
        return bool(task.project and is_project_user(user, task.project))
    if is_developer(user):
        return task.author_id == user.id
    return False


def can_delete_task(user, task):
    if not user or not user.is_authenticated:
        return False
    if user.is_superuser:
        return True
    if is_project_manager(user):
        return bool(task.project and task.project.author_id == user.id)
    if is_team_lead(user):
        return bool(task.project and is_project_user(user, task.project))
    return False


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
        context['can_create_project'] = can_create_project(self.request.user)
        for project in context['projects']:
            project.can_update = can_change_project(self.request.user, project)
            project.can_delete = can_change_project(self.request.user, project)
        return context


class ProjectDetailView(DetailView):
    model = Project
    template_name = 'taskman/project_detail.html'
    context_object_name = 'project'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        tasks = self.object.tasks.filter(is_deleted=False)
        for task in tasks:
            task.can_update = can_change_task(self.request.user, task)
            task.can_delete = can_delete_task(self.request.user, task)
        context['tasks'] = tasks
        context['can_update_project'] = can_change_project(self.request.user, self.object)
        context['can_delete_project'] = can_change_project(self.request.user, self.object)
        context['can_manage_project_users'] = can_manage_project_users(self.request.user, self.object)
        context['can_create_task'] = can_create_task(self.request.user, self.object)
        return context


class ProjectCreateView(LoginRequiredMixin, CreateView):
    model = Project
    form_class = ProjectModelForm
    template_name = 'taskman/project_create.html'
    success_url = reverse_lazy('taskman:task_list')

    def dispatch(self, request, *args, **kwargs):
        if not can_create_project(request.user):
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.author = self.request.user
        response = super().form_valid(form)
        self.object.users.add(self.request.user)
        return response


class ProjectUpdateView(LoginRequiredMixin, UpdateView):
    model = Project
    form_class = ProjectModelForm
    template_name = 'taskman/project_update.html'

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        if not can_change_project(request.user, self.object):
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return reverse('taskman:project_detail', kwargs={'pk': self.object.pk})


class ProjectDeleteView(LoginRequiredMixin, DeleteView):
    model = Project
    template_name = 'taskman/project_delete.html'
    success_url = reverse_lazy('taskman:task_list')

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        if not can_change_project(request.user, self.object):
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)


class ProjectUsersUpdateView(LoginRequiredMixin, UpdateView):
    model = Project
    form_class = ProjectUsersForm
    template_name = 'taskman/project_users_update.html'

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        if not can_manage_project_users(request.user, self.object):
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return reverse('taskman:project_detail', kwargs={'pk': self.object.pk})


class TaskListView(ListView):
    model = Task
    template_name = 'taskman/task_list.html'
    context_object_name = 'tasks'

    def get_queryset(self):
        return Task.objects.filter(is_deleted=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        for task in context['tasks']:
            task.can_update = can_change_task(self.request.user, task)
            task.can_delete = can_delete_task(self.request.user, task)
        return context


class TaskDetailView(DetailView):
    model = Task
    template_name = 'taskman/task_detail.html'
    context_object_name = 'task'

    def get_queryset(self):
        return Task.objects.filter(is_deleted=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['can_update_task'] = can_change_task(self.request.user, self.object)
        context['can_delete_task'] = can_delete_task(self.request.user, self.object)
        return context


class TaskCreateView(LoginRequiredMixin, CreateView):
    model = Task
    form_class = TaskModelForm
    template_name = 'taskman/task_create.html'

    def dispatch(self, request, *args, **kwargs):
        self.project = get_object_or_404(Project, pk=kwargs['project_pk']) if 'project_pk' in kwargs else None
        if not can_create_task(request.user, self.project):
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.author = self.request.user
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

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        if not can_change_task(request.user, self.object):
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return reverse('taskman:task_detail', kwargs={'pk': self.object.pk})


class TaskDeleteView(LoginRequiredMixin, DeleteView):
    model = Task
    template_name = 'taskman/task_delete.html'

    def get_queryset(self):
        return Task.objects.filter(is_deleted=False)

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        if not can_delete_task(request.user, self.object):
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        if self.object.project_id:
            return reverse('taskman:project_detail', kwargs={'pk': self.object.project_id})
        return reverse('taskman:task_list_all')

    def form_valid(self, form):
        self.object.is_deleted = True
        self.object.save()
        return redirect(self.get_success_url())
