from django.conf import settings
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.views import LoginView, LogoutView, PasswordContextMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy, reverse
from django.utils.translation import gettext_lazy as _

from django.shortcuts import render

# Create your views here.
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.debug import sensitive_post_parameters
from django.views.generic import CreateView, TemplateView, FormView, UpdateView, ListView

from posts.models import Post
from users.forms import RegisterForm, UserProfileForm
from users.models import UserProfile


class AllUsersView(ListView):
    model = UserProfile
    context_object_name = 'profiles'
    template_name = 'users/user-list.html'
    paginate_by = 2

    def get_context_data(self, *args, **kwargs):
        context = super(AllUsersView, self).get_context_data(*args, **kwargs)
        return context


class RegisterView(CreateView):
    form_class = RegisterForm
    template_name = 'users/register.html'
    success_url = '/'


class UserLoginView(LoginView):
    template_name = 'users/login.html'


class UserLogoutView(LogoutView):
    template_name = 'users/logout.html'


class UserProfileView(SuccessMessageMixin,UpdateView):
    form_class = UserProfileForm
    model = UserProfile
    template_name = 'users/userprofile.html'
    context_object_name = 'profile'
    success_message = 'The profile has been updated Successfully '

    # success_url = '/'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(UserProfileView, self).get_context_data(**kwargs)
        context['form'] = self.get_form()
        return context

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.save()
        return super(UserProfileView, self).form_valid(form)

    def get_success_url(self):
        return reverse('users:profile', kwargs={'slug': self.object.slug})

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.object.user != request.user:
            return HttpResponseRedirect('/')
        return super(UserProfileView, self).get(request, *args, **kwargs)


class UserPostsProfile(ListView):
    model = Post
    context_object_name = 'userposts'
    template_name = 'users/user-posts.html'
    paginate_by = 2

    def get_context_data(self, *args, **kwargs):
        context = super(UserPostsProfile, self).get_context_data(*args, **kwargs)
        context['user'] = UserProfile.objects.get(user=self.request.user)
        return context

    def get_queryset(self, *args, **kwargs):
        return Post.objects.filter(user=self.request.user).order_by('-id')

    # def get(self, request, *args, **kwargs):
    #     self.object = self.get_object()
    #     if self.object.user != request.user:
    #         return HttpResponseRedirect('/')
    #     return super(UserPostsProfile, self).get(request, *args, **kwargs)


class UserPostsDetail(ListView):
    model = Post
    context_object_name = 'userposts'
    template_name = 'users/user-posts.html'
    paginate_by = 2

    def get_context_data(self, *args, **kwargs):
        context = super(UserPostsDetail, self).get_context_data(*args, **kwargs)
        context['user'] = UserProfile.objects.get(user=self.kwargs['pk'])
        return context

    def get_queryset(self, *args, **kwargs):
        return Post.objects.filter(user=self.kwargs['pk']).order_by('-id')


class PasswordChangeView(PasswordContextMixin, FormView):
    form_class = PasswordChangeForm
    success_url = reverse_lazy('users:password_change_done')
    template_name = 'registration/password_change_form.html'
    title = _('Password change')

    @method_decorator(sensitive_post_parameters())
    @method_decorator(csrf_protect)
    @method_decorator(login_required(login_url='/users/login'))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        form.save()
        # Updating the password logs out all other sessions for the user
        # except the current one.
        update_session_auth_hash(self.request, form.user)
        return super().form_valid(form)


class PasswordChangeDoneView(PasswordContextMixin, TemplateView):
    template_name = 'registration/password_change_done.html'
    title = _('Password change successful')

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)
