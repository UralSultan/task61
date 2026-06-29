from django.urls import path
from accounts.views import login_view, logout_view, MyLoginView, RegisterView
from django.contrib.auth.views import LogoutView



app_name = "accounts"

urlpatterns = [
    path('login/', MyLoginView.as_view(), name='login'),
    # path('login/', login_view, name="login"),
    path('logout/', LogoutView.as_view(), name='logout'),
    # path('logout/', logout_view, name='logout'),
    # path('create/', register_view, name='create')
    path('create/', RegisterView.as_view(), name='create')
]
