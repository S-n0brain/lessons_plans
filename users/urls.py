from django.urls import path
from .views import UserLoginView, UserLogoutView, UserCreateView

app_name = "users"

urlpatterns = [
    path('login/', UserLoginView.as_view(), name='login'),
    path('logout/', UserLogoutView.as_view(), name='logout'),
    path('signup/', UserCreateView.as_view(), name='sign_up'),
]