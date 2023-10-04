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
from django.contrib.auth.forms import PasswordChangeForm
from .models import UserProfile
from django.contrib.auth.models import User
from .models import Category
from .forms import CategoryForm


def user_is_member(user):
    return user.is_superuser or user.groups.filter(name='Member').exists()

def user_is_viewer(user):
    return user.is_superuser or user.groups.filter(name='Viewer').exists()





# def view_profile(request, username):
#     user = get_object_or_404(User, username=username)
#     profile = UserProfile.objects.get(user=user)
#     return render(request, 'blog/profile.html', {'user': user, 'profile': profile})

@login_required
def blog_post_list(request):
    query = request.GET.get('q')
    posts = BlogPost.objects.filter(author=request.user)
    categories = Category.objects.all()
    if query:
        posts = posts.filter(
            Q(title__icontains=query) | Q(content__icontains=query)
        )
        
    context = {
        'categories': categories,  
        'posts': posts,
        'query': query,
    }
    posts = posts.order_by('-pub_date')
    # return render(request, 'blog/post_list.html', {'posts': posts, 'query': query})
    return render(request, 'blog/post_list.html', context)

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

# from django.contrib import messages

def not_allowed(request):
    return render(request, 'blog/not_allowed.html')

@login_required
@user_passes_test(user_is_member, login_url='not_allowed')
def create_blog_post(request):
    if request.method == 'POST':
        form = BlogPostForm(request.POST)
        if form.is_valid():
            blog_post = form.save(commit=False)
            blog_post.author = request.user

            # Save the blog post as draft or published based on the user's choice
            if form.cleaned_data['publish_status'] == 'published':
                blog_post.published = True
            else:
                blog_post.published = False

            # Save the blog post to get an 'id' assigned
            blog_post.save()

            # Get the selected categories as a list of category IDs
            selected_category_ids = request.POST.getlist('categories')

            # Associate the selected categories with the blog post
            for category_id in selected_category_ids:
                category = Category.objects.get(pk=category_id)
                blog_post.categories.add(category)

            return redirect('blog_post_list')
    else:
        form = BlogPostForm()

    return render(request, 'blog/create_post.html', {'form': form})


# def create_blog_post(request):
#     if request.method == 'POST':
#         form = BlogPostForm(request.POST)
#         title = form.cleaned_data['title']
#         content = form.cleaned_data['content']
#         author = request.user
#         publish_status = form.cleaned_data['publish_status']
#         is_draft = request.POST.get('is_draft')

#             if publish_status == 'publish':
#                 return redirect('publish_blog_posts')
#             else:
#                 post = BlogPost(title=title,content=content,author=author,publish_status='draft',)
#                 post.save()
#                 post.categories.set(categories)
#                 return redirect('blog_post_list')
#     return render(request, 'blog/create_post.html', {'form': form})


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
    categories = Category.objects.all()
    
    posts = BlogPost.objects.filter(publish_status='published').order_by('-pub_date')

    if query:
        posts = posts.filter(Q(title__icontains=query) | Q(content__icontains=query))

    context = {
        'categories': categories,  
        'posts': posts,
        'query': query,
        }
    return render(request, 'blog/publish.html', context)


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




@login_required
def category_list(request):
    categories = Category.objects.all()
    return render(request, 'category/category_list.html', {'categories': categories})

@login_required
def category_list1(request):
    categories = Category.objects.all()
    return render(request, 'category/category.html', {'categories': categories})

@login_required
def Category_create(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            category = form.save()
            messages.success(request, 'Your category was successfully created!')
            return redirect('category_list')
    else:
        form = CategoryForm()
        return render(request ,'category/category_create.html', {'form': form} )
        
        
@login_required
def category_edit(request, category_id):
    category = get_object_or_404(Category, pk=category_id)
    if request.method == 'POST':
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            messages.success(request, 'Category updated successfully.')
            return redirect('category_list')
    else:
        form = CategoryForm(instance=category)
    return render(request, 'category/category_edit.html', {'form': form, 'category': category})


@login_required
def category_delete(request, category_id):
    category = get_object_or_404(Category, pk=category_id)
    if request.method == 'POST':
        category.delete()
        messages.success(request, 'Category deleted successfully.')
        return redirect('category_list')
    return render(request, 'category/category_delete.html', {'category': category})


@login_required
def category_post_list(request, category_id):
    category = get_object_or_404(Category, pk=category_id)
    posts = BlogPost.objects.filter(categories=category, published=True)
    return render(request, 'category/post_category.html', {'category': category, 'posts': posts})


# from django.shortcuts import render
# from .models import Category, BlogPost

# def all_categories_and_posts(request):
#     categories = Category.objects.all()
#     category_posts = {}

#     for category in categories:
#         posts = BlogPost.objects.filter(categories=category, published=True)
#         category_posts[category] = posts

#     return render(request, 'category/all_category&post.html', {'categories': categories, 'category_posts': category_posts})




