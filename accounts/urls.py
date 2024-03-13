from django.urls import path

from accounts import views

urlpatterns = [
    path('', views.RedirectIndex.as_view(), name='index'),
    path('index/', views.Index.as_view(), name='index'),
    path('login/', views.Login.as_view(), name='login'),
    path('register/', views.Register.as_view(), name='register'),
    path('logout/', views.logout, name='logout'),
    path('createpost/', views.CreatePost.as_view(), name='createpost'),
    path('user/<str:username>/', views.UserProfile.as_view(), name='userprofile')
]
