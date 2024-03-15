from django.urls import path

from accounts import views
from accounts.views import CommentView, EditProfile

urlpatterns = [
    path('', views.RedirectIndex.as_view(), name='index'),
    path('index/', views.Index.as_view(), name='index'),
    path('login/', views.Login.as_view(), name='login'),
    path('register/', views.Register.as_view(), name='register'),
    path('logout/', views.logout, name='logout'),
    path('createpost/', views.CreatePost.as_view(), name='createpost'),
    path('user/<str:username>/', views.UserProfile.as_view(), name='userprofile'),
    path('follow/', views.Follow.as_view(), name='follow'),
    path('comment/', CommentView.as_view(), name='comment'),
    path('edit/', EditProfile.as_view(), name='editprofile'),
    path('like/<int:pk>', views.Like.as_view(), name='like')
]
