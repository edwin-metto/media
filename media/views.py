from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponse
from django.core.exceptions import PermissionDenied
from .models import Post, Like, Comment, Follow
from .forms import PostForm, CommentForm
from django.contrib.auth.models import User
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import UserUpdateForm, ProfileUpdateForm


def home(request):
    posts = Post.objects.all()
    for post in posts:
        post.top_level_comments = post.comments.filter(parent=None)  
    return render(request, 'home.html', {'posts': posts})

@login_required
def user_profile(request, user_id):
    user = get_object_or_404(User, id=user_id)
    return render(request, 'user_profile.html', {'user_profile': user})



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
    post = get_object_or_404(Post, id=post_id)
    if Like.objects.filter(user=request.user, post=post).exists():
        likes = Like.objects.filter(post=post).select_related('user')
        liked_users = [like.user.username for like in likes]
        return JsonResponse({'message': 'You already liked this post.', 'likes': liked_users}, status=400)

    Like.objects.create(user=request.user, post=post)
    return redirect('home')


@login_required
def comment_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.method == 'POST':
        content = request.POST.get('content')
        parent_id = request.POST.get('parent_id', None)
        parent = Comment.objects.filter(id=parent_id).first() if parent_id else None
        Comment.objects.create(user=request.user, post=post, parent=parent, content=content)
    return redirect('home')



@login_required
def delete_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if post.user != request.user:
        raise PermissionDenied
    post.delete()
    return redirect('home')


@login_required
def get_post_likes(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    likes = Like.objects.filter(post=post).select_related('user')
    liked_users = [like.user.username for like in likes]
    return JsonResponse({'post': post.id, 'likes': liked_users})


@login_required
def user_followers_view(request, user_id):
    user = get_object_or_404(User, id=user_id)
    followers = Follow.objects.filter(followed=user)
    context = {'user_profile': user, 'followers': followers}
    return render(request, 'followers.html', context)


@login_required
def user_following_view(request, user_id):
    user = get_object_or_404(User, id=user_id)
    following = Follow.objects.filter(follower=user)
    context = {'user_profile': user, 'following': following}
    return render(request, 'following.html', context)


@login_required
def follow_user(request, user_id):
    followed_user = get_object_or_404(User, id=user_id)
    if request.user != followed_user: 
        follow, created = Follow.objects.get_or_create(follower=request.user, followed=followed_user)
        if created:
            return JsonResponse({'message': 'Followed successfully!'}, status=200)
        return JsonResponse({'message': 'You already follow this user.'}, status=400)
    return JsonResponse({'message': 'You cannot follow yourself.'}, status=400)


@login_required
def unfollow_user(request, user_id):
    followed_user = get_object_or_404(User, id=user_id)
    follow = Follow.objects.filter(follower=request.user, followed=followed_user)
    if follow.exists():
        follow.delete()
        return JsonResponse({'message': 'Unfollowed successfully!'}, status=200)
    return JsonResponse({'message': 'You are not following this user.'}, status=400)



@login_required
def search_users(request):
    query = request.GET.get('q', '')
    users = User.objects.filter(username__icontains=query).exclude(id=request.user.id) if query else None
    followed_users = Follow.objects.filter(follower=request.user).values_list('followed_id', flat=True)

    context = {
        'query': query,
        'users': users,
        'followed_users': followed_users,
    }
    return render(request, 'search_users.html', context)



@login_required
def toggle_follow(request, user_id):
    target_user = get_object_or_404(User, id=user_id)
    if request.user == target_user:
        return JsonResponse({'error': 'You cannot follow yourself.'}, status=400)

    follow, created = Follow.objects.get_or_create(follower=request.user, followed=target_user)
    if not created:
        follow.delete()
        return JsonResponse({'message': 'Unfollowed successfully.'})
    return JsonResponse({'message': 'Followed successfully.'})


