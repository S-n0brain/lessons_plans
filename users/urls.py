from django.urls import path
from .views import (UserLoginView, UserLogoutView, UserCreateView, UserPasswordChangeView,
                    UserPasswordChangeDoneView, UserPasswordResetView,
                    UserPasswordResetDoneView, UserPasswordResetConfirmView, UserPasswordResetCompleteView)
app_name = "users"

urlpatterns = [
    path('login/', UserLoginView.as_view(), name='login'),
    path('logout/', UserLogoutView.as_view(), name='logout'),
    path('signup/', UserCreateView.as_view(), name='sign_up'),
    path('password_change/', UserPasswordChangeView.as_view(), name='password_change'),
    path('password_change_done/', UserPasswordChangeDoneView.as_view(), name='password_change_done'),
    path('password_reset/', UserPasswordResetView.as_view(), name='password_reset'),
    path('password_reset_done/', UserPasswordResetDoneView.as_view(), name='password_reset_done'),
    path('password_reset/<uidb64>/<token>/', UserPasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('password_reset_complete/', UserPasswordResetCompleteView.as_view(), name='password_reset_complete'),
]