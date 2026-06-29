from django.urls import path
from accounts.views import login_view, logout_view, RegisterView
from django.contrib.auth.views import LoginView, LogoutView



app_name = "accounts"

urlpatterns = [
    path('login/', LoginView.as_view(template_name="accounts/login.html"), name='login'),
    # path('login/', login_view, name="login"),
    path('logout/', LogoutView.as_view(), name='logout'),
    # path('logout/', logout_view, name='logout'),
    # path('create/', register_view, name='create')
    path('create/', RegisterView.as_view(), name='create')
]
