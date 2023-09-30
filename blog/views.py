from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import BlogPost, Comment
from django.shortcuts import render, redirect, get_object_or_404
from .forms import BlogPostForm
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib import messages  
from django.utils import timezone
from .models import BlogPost
from django.db.models import Q
from django.contrib.auth.models import Group, Permission
from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import render, redirect
from .models import BlogPost
from django.http import HttpResponse
from django.contrib.auth.views import PasswordChangeView
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash



def user_is_member(user):
    return user.is_superuser or user.groups.filter(name='Member').exists()

def user_is_viewer(user):
    return user.is_superuser or user.groups.filter(name='Viewer').exists()


@login_required
def blog_post_list(request):
    query = request.GET.get('q')
    posts = BlogPost.objects.filter(author=request.user)
    if query:
        posts = posts.filter(
            Q(title__icontains=query) | Q(content__icontains=query)
        )
    posts = posts.order_by('-pub_date')
    return render(request, 'blog/post_list.html', {'posts': posts, 'query': query})

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            group_name = request.POST.get('groups')
            
            group, created = Group.objects.get_or_create(name=group_name)
            user.groups.add(group)

            login(request, user)
            messages.success(request, 'Registration successful. You are now logged in.')
            return redirect('blog_post_list')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'{field}: {error}')
    else:
        form = UserCreationForm()
    return render(request, 'blog/register.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, 'Login successful.')
            return redirect('blog_post_list')

    else:
        form = AuthenticationForm()
    return render(request, 'blog/login.html', {'form': form})

from django.contrib import messages

def not_allowed(request):
    return render(request, 'blog/not_allowed.html')

@login_required
@user_passes_test(user_is_member, login_url='not_allowed')
def create_blog_post(request):
    if request.method == 'POST':
        title = request.POST['title']
        content = request.POST['content']
        author = request.user
        publish_status = request.POST.get('publish_status')
        is_draft = request.POST.get('is_draft')
        
        if publish_status == 'publish':
            post = BlogPost(title=title, content=content, author=author, publish_status='published')
            return redirect('publish_blog_posts') 
        else:
            post = BlogPost(title=title, content=content, author=author, publish_status='draft')
            post.save()
        return redirect('blog_post_list')  
        
            
    
        
    return render(request, 'blog/create_post.html')


def view_blog_post(request, post_id):
    post = BlogPost.objects.get(pk=post_id)
    comments = Comment.objects.filter(post=post)
    return render(request, 'blog/view.post.html', {'post': post, 'comments': comments})

@login_required
@user_passes_test(user_is_member, login_url='not_allowed')
def add_comment(request, post_id):
    post = BlogPost.objects.get(pk=post_id)
    if request.method == 'POST':
        text = request.POST['comment_text']
        author = request.user
        comment = Comment(post=post, author=author, text=text)
        comment.save()
        return redirect('view_blog_post', post_id=post_id)
    return redirect('view_blog_post', post_id=post_id)




@login_required 
def publish_blog_post(request):
    query = request.GET.get('q')
    
    posts = BlogPost.objects.filter(publish_status='published').order_by('-pub_date')

    if query:
        posts = posts.filter(Q(title__icontains=query) | Q(content__icontains=query))

    return render(request, 'blog/publish.html', {'posts': posts})


@login_required
@user_passes_test(user_is_member, login_url='not_allowed')
def delete_blog_post(request, post_id):
    post = get_object_or_404(BlogPost, pk=post_id)
    if request.method == 'POST':
        post.delete()
        return redirect('blog_post_list')
    return render(request, 'blog/post_delete.html', {'post': post})



@login_required
@user_passes_test(user_is_member, login_url='not_allowed')
def update_blog_post(request, post_id):
    post = get_object_or_404(BlogPost, pk=post_id)

    if request.method == 'POST':
        form = BlogPostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            return redirect('view_blog_post', post_id=post_id)
    else:
        form = BlogPostForm(instance=post)

    return render(request, 'blog/post_edit.html', {'form': form, 'post': post})


@login_required
def password_change(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, 'Your password was successfully updated!')
            return redirect('password_change')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'change_password.html', {'form': form})