from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.login_view, name='login'),
    path('signup/', views.signup, name='signup'),
    path('logout/', views.logout_view, name='logout'),
    path('create_post/', views.create_post, name='create_post'),
    path('like/<int:post_id>/', views.like_post, name='like_post'),
    path('comment/<int:post_id>/', views.comment_post, name='comment_post'),
    path('delete_post/<int:post_id>/', views.delete_post, name='delete_post'),
     path('follow/<int:user_id>/', views.follow_user, name='follow_user'),
    path('unfollow/<int:user_id>/', views.unfollow_user, name='unfollow_user'),
    path('followers/<int:user_id>/', views.user_followers_view, name='user_followers'),
    path('following/<int:user_id>/', views.user_following_view, name='user_following'),
    path('search/', views.search_users, name='search_users'),
    path('user/<int:user_id>/', views.user_profile, name='user_profile'),
    path('toggle-follow/<int:user_id>/', views.toggle_follow, name='toggle_follow'),
    

]