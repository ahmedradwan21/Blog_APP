from django.urls import path
from . import views
from django.contrib.auth.views import PasswordChangeView
from django.contrib.auth import views as auth_views
from .views import category_list, category_post_list,category_list1

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
    path('change-password/', auth_views.PasswordChangeView.as_view(template_name='change_password.html',success_url='/password-change-done/'  ), name='password_change'),
    path('password-change-done/', auth_views.PasswordChangeDoneView.as_view(template_name='password_change_done.html'), name='password_change_done'),
    
    
    
    path('blog/categories/', category_list, name='category_list'),
    path('blog/category/', category_list1, name='category_list1'),
    path('blog/categories/<int:category_id>/', category_post_list, name='category_post_list'),
    path('blog/create_category/', views.Category_create, name='category_create'),
    path('blog/edit_category/<int:category_id>/', views.category_edit, name='category_edit'),
    path('blog/delete_category/<int:category_id>/', views.category_delete, name='category_delete'),
    # path('all_categories_and_posts/', views.all_categories_and_posts, name='all_categories_and_posts'),
    # path('categories/<int:category_id>/',views.category_post_list, name='category_post_list'),
    # path('blog/category/<int:category_id>/', views.category_post_list, name='category_post_list'),
    # path('blog/categories/', views.category_list, name='category_list_post'),
]
