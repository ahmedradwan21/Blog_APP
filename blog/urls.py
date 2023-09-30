from django.urls import path
from . import views
from django.contrib.auth.views import PasswordChangeView
from django.contrib.auth import views as auth_views

from django.contrib.auth.views import LogoutView
urlpatterns = [
    path('', views.blog_post_list, name='blog_post_list'),
    path('<int:post_id>/', views.view_blog_post, name='view_blog_post'),
    path('create/', views.create_blog_post, name='create_blog_post'),
    path('<int:post_id>/edit/', views.update_blog_post, name='update_blog_post'),
    path('<int:post_id>/delete/', views.delete_blog_post, name='delete_blog_post'),
    path('<int:post_id>/comment/', views.add_comment, name='add_comment'),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/',LogoutView.as_view(next_page='login'), name='logout'),
    path('publish/', views.publish_blog_post, name='publish_blog_posts'),
    path('not_allowed/', views.not_allowed, name='not_allowed'),
    path('change-password/', PasswordChangeView.as_view(), name='password_change'),
        path('change-password/', auth_views.PasswordChangeView.as_view(
        template_name='change_password.html',
        success_url='/password-change-done/'  # Define your custom success URL here
    ), name='password_change'),
    path('password-change-done/', auth_views.PasswordChangeDoneView.as_view(
        template_name='password_change_done.html'
    ), name='password_change_done'),
]
