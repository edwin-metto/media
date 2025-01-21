from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import Post, Like, Comment
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from .forms import PostForm, CommentForm
from django.core.exceptions import PermissionDenied


def home(request):
    posts = Post.objects.all()
    return render(request, 'home.html', {'posts': posts})


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})


def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'signup.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('login')


@login_required
def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.save()
            return redirect('home')
    else:
        form = PostForm()
    return render(request, 'create_post.html', {'form': form})


@login_required
def like_post(request, post_id):
    post = Post.objects.get(id=post_id)
    if Like.objects.filter(user=request.user, post=post).exists():
        return HttpResponse('You already liked this post.', status=400)
    Like.objects.create(user=request.user, post=post)
    return redirect('home')


@login_required
def comment_post(request, post_id):
    post = Post.objects.get(id=post_id)
    if request.method == 'POST':
        content = request.POST['content']
        Comment.objects.create(user=request.user, post=post, content=content)
    return redirect('home')


@login_required
def delete_post(request, post_id):
    post = Post.objects.get(id=post_id)
    if post.user != request.user:
        raise PermissionDenied
    post.delete()
    return redirect('home')
