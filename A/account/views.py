from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views import View
from home.models import Post
from .forms import RegisterUserForm, LoginUserForm
from django.contrib.auth.mixins import LoginRequiredMixin
from home.forms import PostCreateUpdateForm, CommentCreateForm, CommentReplyCreateForm
from django.contrib.auth import views as auth_view
from .models import Relation


class RegisterUserView(View):
    form_class = RegisterUserForm
    template_name = 'account/register_user.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            messages.warning(request, 'you cannot register again!!!', extra_tags='warning')
            return redirect('home:home')
        else:
            return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, context={'form': form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            User.objects.create_user(cd['username'], email=cd['email'], password=cd['password'])
            messages.success(request, 'successfully registered', extra_tags='success')
            return redirect('home:home')
        return render(request, self.template_name, context={'form': form})


class LoginUserView(View):
    form_class = LoginUserForm
    template_name = 'account/login_form.html'

    def setup(self, request, *args, **kwargs):
        self.next = request.GET.get('next')
        return super().setup(request, *args, **kwargs)

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            messages.warning(request, 'you cannot log in again!!!')
            return redirect('home:home')
        else:
            return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        form = self.form_class()
        return render(request, 'account/login_form.html', context={'form': form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, 'logged in successfully', extra_tags='success')
                if self.next:
                    return redirect(self.next)
                return redirect('home:home')
            messages.error(request, 'this user pass is wrong!!!', extra_tags='danger')
        return render(request, self.template_name, context={'form': form})


class LogoutUserView(LoginRequiredMixin, View):
    def get(self, request):
        logout(request)
        messages.success(request, 'successfully logged out', extra_tags='success')
        return redirect('home:home')


class ProfileUserView(LoginRequiredMixin, View):
    def get(self, request, user_id):
        user = get_object_or_404(User, pk=user_id)
        posts = Post.objects.filter(user=user)

        is_following = Relation.objects.filter(from_user=request.user, to_user=user).exists()
        return render(request, 'account/profile_user.html',
                      context={'posts': posts, 'user': user, 'is_following': is_following})


class DetailPostView(View):
    class_form_comment = CommentCreateForm

    def setup(self, request, *args, **kwargs):
        self.page_post = get_object_or_404(Post, pk=kwargs['post_id'])
        return super().setup(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        comment_reply_form = CommentReplyCreateForm
        pcomments = self.page_post.pcomments.filter(is_reply=False)
        return render(request, 'account/post_detail.html', context={'post': self.page_post, 'pcomments': pcomments,
                                                                    'comment_create_form': self.class_form_comment,
                                                                    'comment_reply_form': comment_reply_form})

    @method_decorator(login_required)
    def post(self, request, post_id):
        form = self.class_form_comment(request.POST)
        if form.is_valid():
            new_form = form.save(commit=False)
            new_form.user = request.user
            new_form.post = self.page_post
            new_form.save()
            messages.success(request, 'comment submitted successfully')
            return redirect('account:detail', post_id)


class DeletePostView(LoginRequiredMixin, View):

    def setup(self, request, *args, **kwargs):
        self.post_instance = get_object_or_404(Post, pk=kwargs.get('post_id'))
        return super().setup(request, *args, **kwargs)

    def dispatch(self, request, *args, **kwargs):
        post = self.post_instance
        if not request.user.id == post.user.id:
            messages.error(request, 'the post does not belong to you!!!', extra_tags='danger')
            return redirect('account:profile', post.user.id)
        else:
            return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        post = self.post_instance

        post.delete()
        messages.success(request, 'successfully deleted post', 'success')
        return redirect('account:profile', post.user.id)


class UpdatePostView(LoginRequiredMixin, View):
    form_class = PostCreateUpdateForm

    def setup(self, request, *args, **kwargs):
        self.post_instance = get_object_or_404(Post, pk=kwargs.get('post_id'))
        return super().setup(request, *args, **kwargs)

    def dispatch(self, request, *args, **kwargs):
        post = self.post_instance
        if not request.user.id == post.user.id:
            messages.error(request, 'the post does not belong to you!!!', extra_tags='danger')
            return redirect('account:profile', post.user.id)
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        post = self.post_instance
        form = self.form_class(instance=post)
        return render(request, 'account/update_post.html', context={'form': form})

    def post(self, request, post_id):
        post = self.post_instance
        form = self.form_class(request.POST, instance=post)
        if form.is_valid():
            form.save()
            messages.success(request, 'successfully updated', extra_tags='success')
            return redirect('account:detail', post_id)
        return render(request, 'account/update_post.html', context={'form': form})


class CreatePostView(LoginRequiredMixin, View):
    form_class = PostCreateUpdateForm

    def get(self, request):
        form = self.form_class
        return render(request, 'account/create_post.html', context={'form': form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            new_post = form.save(commit=False)
            new_post.user = request.user
            form.save()
            messages.success(request, 'successfully created', 'success')
            return redirect('account:detail', new_post.id)
        return render(request, 'account/create_post.html', context={'form': form})


class UserPasswordResetView(auth_view.PasswordResetView):
    template_name = 'account/password_reset_form.html'
    success_url = reverse_lazy('account:password_reset_done')
    email_template_name = 'account/password_reset_email.html'


class UserPasswordResetDoneView(auth_view.PasswordResetDoneView):
    template_name = 'account/password_reset_done.html'


class UserPasswordResetConfirmView(auth_view.PasswordResetConfirmView):
    template_name = 'account/password_reset_confirm.html'
    success_url = reverse_lazy('account:password_reset_complete')


class UserPasswordResetCompleteView(auth_view.PasswordResetCompleteView):
    template_name = 'account/password_reset_complete.html'


class FollowUserView(LoginRequiredMixin, View):
    def get(self, request, user_id):
        user = User.objects.get(id=user_id)
        is_exist_relation = Relation.objects.filter(from_user=request.user, to_user=user).exists()

        if is_exist_relation:
            messages.error(request, f'You cannot follow {user.username} again!!!', extra_tags='danger')
        else:
            Relation(from_user=request.user, to_user=user).save()
            messages.success(request, f'you are following {user.username}', 'success')
        return redirect('account:profile', user_id)


class UnfollowUserView(LoginRequiredMixin, View):
    def get(self, request, user_id):
        user = User.objects.get(id=user_id)
        relation = Relation.objects.filter(from_user=request.user, to_user=user)

        if relation.exists():
            relation.delete()
            messages.success(request, f'you do not follow {user.username}', extra_tags='success')
        else:
            messages.error(request, f'you are now following {user.username}', extra_tags='danger')
        return redirect('account:profile', user_id)

