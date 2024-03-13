from django.shortcuts import render, redirect, get_object_or_404
from django.views import View

from accounts.forms import SignUpForm, LoginForm, PostForm
from accounts.models import Post, User
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout as auth_logout


# Create your views here.


class Index(View):
    def get(self, request):
        posts = Post.objects.all()
        form = PostForm()
        return render(request, 'accounts/index.html', {'form': form, 'posts': posts})


class RedirectIndex(View):
    def get(self, request):
        return redirect('/index/')


def logout(request):
    auth_logout(request)
    return redirect('/index/')


class Login(View):
    def get(self, request):
        form = LoginForm()
        return render(request, 'accounts/login.html', {'form': form, 'login': True})

    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is None:
                return render(request, 'accounts/login.html', {'form': form})
            login(request, user)
            return redirect('/index/')
        return render(request, 'accounts/login.html', {'form': form})


class UserProfile(View):
    def get(self, request, *args, **kwargs):
        username = kwargs.get('username')
        user = get_object_or_404(User, username=username)
        posts = Post.objects.filter(author=user)
        postCount = posts.count()
        return render(request, 'accounts/profile.html', {'user': user, 'posts': posts, 'postCount': postCount})
        # user = User.objects.get(username=username)


class EditProfile(View):
    def get(self, request, *args, **kwargs):
        pass


class Register(View):
    def get(self, request):
        form = SignUpForm()
        return render(request, 'accounts/login.html', {'form': form, 'login': False})

    def post(self, request):
        # first_name = request.POST['fname']
        # last_name = request.POST['lname']
        # username = request.POST['uname']
        # email = request.POST['email']
        # password = request.POST['password']
        # try:
        #     user = User.objects.create_user(first_name=first_name, last_name=last_name, username=username,
        #                                     email=email)
        #     user.set_password(password)
        # except:
        #     pass
        # return HttpResponse("aaaaaa")
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.set_password(user.password)
            user.save()
            login(request, user)
            return redirect("/index/")
        return render(request, 'accounts/login.html', {'form': form, "login": False})


class CreatePost(View):
    def post(self, request):
        form = PostForm(request.POST)
        if form.is_valid():
            body = form.cleaned_data['body']
            image = request.FILES['image']  # Get the uploaded image
            post = Post.objects.create(body=body, author=request.user)
            if image:
                post.image = image
                post.save()
        return redirect('/index/')
