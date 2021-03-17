from django.shortcuts import render, redirect
from django.contrib import messages
from django.views.generic import DetailView
from .forms import UserRegistrationForm, UserUpdateForm, ProfileUpdateForm
from django.contrib.auth.decorators import login_required
from home.models import Post
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin

# Create your views here.

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Your account has been created, {username}. Now you can log in!', )
            return redirect('login')
    else:
        form = UserRegistrationForm()
    return render(request, 'users/registration.html', {'form': form, 'title': 'Registration'})

class AuthorDetailView(LoginRequiredMixin, DetailView):
    model = User

    def get_context_data(self, **kwargs):
        context = super(AuthorDetailView, self).get_context_data(**kwargs)
        context['posts'] = Post.objects.all()
        context['author_view'] = True
        return context

@login_required()
def profile(request):
    context = {
        'posts': Post.objects.all(),
        'title': 'My Profile',
    }
    return render(request, 'users/profile.html', context)

@login_required()
def profile_update(request):
    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Your account has been successfully updated!')
            return redirect('profile')
        else:
            messages.error(request, 'Your changes cannot be saved, something is wrong!')
    else:
        user_form = UserUpdateForm(instance=request.user)
        profile_form = ProfileUpdateForm(instance=request.user.profile)
    context = {
        'posts': Post.objects.all(),
        'title': 'Update Profile',
        'user_form': user_form,
        'profile_form': profile_form
    }
    return render(request, 'users/update.html', context)