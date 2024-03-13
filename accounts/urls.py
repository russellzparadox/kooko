from django.urls import path

from accounts import views

urlpatterns = [
    path('', views.RedirectIndex.as_view(), name='index'),
    path('index/', views.Index.as_view(), name='index'),
    path('login/', views.Login.as_view(), name='login'),
]
