from django.urls import path
from . import views

app_name = 'account'
urlpatterns = [
    path('register/', views.RegisterUserView.as_view(), name='register'),
    path('login/', views.LoginUserView.as_view(), name='login'),
    path('logout/', views.LogoutUserView.as_view(), name='logout'),
    path('profile/<int:user_id>/', views.ProfileUserView.as_view(), name='profile'),
    path('post/detail/<int:post_id>/', views.DetailPostView.as_view(), name='detail'),
    path('post/delete/<int:post_id>/', views.DeletePostView.as_view(), name='delete'),
    path('post/update/<int:post_id>/', views.UpdatePostView.as_view(), name='update'),
    path('post/create/', views.CreatePostView.as_view(), name='create'),
    path('reset/', views.UserPasswordResetView.as_view(), name='reset'),
    path('reset/done', views.UserPasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/confirm/<uidb64>/<token>/', views.UserPasswordResetConfirmView.as_view(),
         name='password_reset_confirm'),
    path('reset/complete', views.UserPasswordResetCompleteView.as_view(), name='password_reset_complete'),
    path('follow/<int:user_id>/', views.FollowUserView.as_view(), name='follow'),
    path('unfollow/<int:user_id>/', views.UnfollowUserView.as_view(), name='unfollow'),

]
