from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .models import Post
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .web_scraper import scrape as scrape_function
from .web_scraper import read_file

# Create your views here.

def home(request):
    content = {
        'posts': Post.objects.all(),
        'title': 'Home'
    }
    return render(request, 'home/home.html', content)

class PostListView(ListView):
    model = Post
    template_name = 'home/home.html'
    context_object_name = 'posts'
    ordering = ['-date']

class PostDetailView(LoginRequiredMixin, DetailView):
    model = Post

class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False

class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = '/'

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False

def info(request):
    return render(request, 'home/info.html', {'title': 'Info'})

@login_required()
def scrape(request):

    scrape_function()
    items = read_file()

    context = {
        'title': 'Deals',
        'items': items
    }

    return render(request, 'home/web_scraper.html', context)