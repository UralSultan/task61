from django.contrib.auth import authenticate, login, logout, get_user_model
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.generic import CreateView
from .forms import MyUserCreationForm
from django.contrib.auth.models import User

def login_view(request):
    context = {}
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('taskman:task_list')
        else:
            context['has_error'] = True
    return render(request, 'accounts/login.html', context=context)

def logout_view(request):
    logout(request)
    return redirect('taskman:task_list')


# def register_view(request, *args, **kwargs):
#     if request.method == 'POST':
#         form = MyUserCreationForm(data=request.POST)
#         if form.is_valid():
#             user = form.save()
#             login(request, user)
#             return redirect('taskman:task_list')
#
#     else:
#         form = MyUserCreationForm()
#     return render(request, 'accounts/user_create.html', context={'form': form})

class RegisterView(CreateView):
    model = User
    template_name = 'accounts/user_create.html'
    form_class = MyUserCreationForm

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect(self.get_success_url())


    def get_success_url(self):
        next_url = self.request.GET.get('next')
        if not next_url:
            next_url = self.request.POST.get('next')
        if not next_url:
            next_url = reverse('index')
        return next_url