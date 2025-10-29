from django.views.generic import ListView, DetailView
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views import generic
from django.contrib import messages

from .models import NewsArticle

# Home page: Displays a list of news articles
class NewsListView(ListView):
    model = NewsArticle
    template_name = 'news/index.html'
    context_object_name = 'articles'
    # Show only published articles, newest first
    queryset = NewsArticle.objects.filter(is_published=True)[:9] 

# Detail page: Displays the full article content
class NewsDetailView(DetailView):
    model = NewsArticle
    template_name = 'news/detail.html'
    context_object_name = 'article'
    slug_field = 'slug'
    slug_url_kwarg = 'article_slug'

class SignUpView(generic.CreateView):
    form_class = UserCreationForm
    # We will use get_success_url instead of reverse_lazy('login')
    template_name = 'registration/signup.html'
    
    # NEW: Override this method to add the success message
    def get_success_url(self):
        # Add the success message before redirecting to the login page
        messages.success(self.request, '🎉 Your account is created! You can now log in below.')
        return reverse_lazy('login')