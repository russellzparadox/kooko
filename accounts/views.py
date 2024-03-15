from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from accounts.forms import SignUpForm, LoginForm, PostForm, EditProfileForm
from accounts.models import Post, User, Comment, Likes
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout as auth_logout


# Create your views here.


class Index(View):
    def get(self, request):
        posts = Post.objects.all()
        # posts.comments.all()
        form = PostForm()
        return render(request, 'accounts/index.html', {'form': form, 'posts': posts})


class CommentView(LoginRequiredMixin, View):
    def post(self, request):
        body = request.POST.get('comment')
        post_id = request.POST.get('post')
        post = Post.objects.get(pk=post_id)
        Comment.objects.create(body=body, parent=post, author=request.user)
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))


class RedirectIndex(View):
    def get(self, request):
        return redirect('/index/')


def logout(LoginRequiredMixin, request):
    auth_logout(request)
    return redirect('/index/')


class Like(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        kook = kwargs.get('pk', None)
        # kook = request.POST.get('pk', None)
        kook = Post.objects.get(pk=kook)

        if Likes.objects.filter(user=request.user, post=kook).exists():
            Likes.objects.filter(user=request.user, post=kook).delete()
            kook.likeCount = kook.likeCount - 1
            kook.save()
            return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
        Likes.objects.create(user=request.user, post=kook)
        kook.likeCount = kook.likeCount + 1
        kook.save()
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))


class Login(View):
    def get(self, request):
        if request.user.is_authenticated:
            return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
        form = LoginForm()
        return render(request, 'accounts/login.html', {'form': form, 'login': True})

    def post(self, request):
        if request.user.is_authenticated:
            return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

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
        post_count = posts.count()
        # if request.user.is_authenticated:
        itself = request.user.username == username
        followed = False
        if request.user.is_authenticated:
            followed = request.user.follows.filter(username=username).count()
        followers = user.followers.count()
        following = user.follows.count()
        return render(request, 'accounts/profile.html',
                      {'user_profile': user, 'posts': posts, 'postCount': post_count, 'followed': followed,
                       'following': following, 'followers': followers, 'itself': itself})
        # user = User.objects.get(username=username)


class comment(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        body = request.POST.get('body')
        parent_id = request.POST.get('parent')
        post = Post.objects.get(id=parent_id)
        comment = Comment.objects.create(body=body, author=request.user, parent=post)
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))


class Follow(LoginRequiredMixin, View):
    def post(self, request):
        username = request.POST.get('to')
        user = request.user
        user2 = User.objects.get(username=username)
        if user2.username == user.username:
            return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
        if user.follows.filter(username=username):
            user.follows.remove(user2)
        else:
            user.follows.add(user2)
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))


class EditProfile(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        user_form = EditProfileForm(instance=request.user)
        return render(request, 'accounts/editProfile.html', {'user_form': user_form})
        pass

    def post(self, request):
        user_form = EditProfileForm(request.POST, instance=request.user)
        pp = request.FILES.get('pp', None)
        user = User.objects.get(username=request.user.username)

        # if user_form.is_valid() and profile_form.is_valid():
        #     user_form.save()
        #     profile_form.save()
        #     return redirect('/index/')
        #
        # firstname = request.POST.get('first_name', None)
        # lastname = request.POST.get('last_name', None)
        # email = request.POST.get('email', None)
        # description = request.POST.get('description', None)
        # user.first_name = firstname
        # user.lastname = lastname
        # user.email = email
        # user.description = description

        if pp:
            user.picture = pp
        user.save()
        return redirect('/index/')


class Register(View):

    def get(self, request):
        if request.user.is_authenticated:
            return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

        form = SignUpForm()
        return render(request, 'accounts/login.html', {'form': form, 'login': False})

    def post(self, request):
        if request.user.is_authenticated:
            return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

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


class CreatePost(LoginRequiredMixin, View):
    def post(self, request):
        form = PostForm(request.POST)
        if form.is_valid():
            body = form.cleaned_data['body']
            image = request.FILES.get('image', None)
            post = Post.objects.create(body=body, author=request.user)
            if image:
                post.image = image
                post.save()
        return redirect('/index/')
