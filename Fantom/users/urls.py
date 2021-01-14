from django.urls import path

from users.views import RegisterView, UserLoginView, UserLogoutView, PasswordChangeView, PasswordChangeDoneView, \
    UserProfileView, UserPostsProfile, UserPostsDetail, AllUsersView
from django.contrib.auth import views as AuthView

app_name = 'users'
urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('myprofile/', UserPostsProfile.as_view(), name='myprofile'),
    path('user-posts/<int:pk>/', UserPostsDetail.as_view(), name='user-posts'),
    path('profile/<slug:slug>', UserProfileView.as_view(), name='profile'),
    path('all-users/', AllUsersView.as_view(), name='all-users'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('logout/', UserLogoutView.as_view(), name='logout'),
    path('password-change/', PasswordChangeView.as_view(), name='change_password'),
    path('password-change-done/', PasswordChangeDoneView.as_view(), name='change_password_done'),
]
