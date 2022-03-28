from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView
from .forms import *
from .models import *


class Home(ListView):
    model = Post
    template_name = 'main/home.html'
    context_object_name = 'posts'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['cats'] = Category.objects.all()
        context['slider'] = Post.objects.all().reverse()[:3]
        return context


class HomeCat(ListView):
    model = Post
    template_name = 'main/home.html'
    context_object_name = 'posts'

    def get_queryset(self):
        return Post.objects.filter(cat__slug=self.kwargs['cat_slug'], is_published=True)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['cats'] = Category.objects.all()
        context['selected'] = self.kwargs['cat_slug']
        context['slider2'] = Post.objects.all().reverse()[:4]
        return context


class ShowPost(DetailView, CreateView):
    form_class = CommentForm
    model = Post
    template_name = 'main/single.html'
    slug_url_kwarg = 'post_slug'
    pk_url_kwarg = 'post_id'
    context_object_name = 'post'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['cats'] = Category.objects.all()
        context['selected'] = self.kwargs['cat_slug']
        context['comm_count'] = self.object.Comments.count()
        context['comments'] = self.object.Comments.filter(active=True)
        return context

    def form_valid(self, form):
        comm = form.save(commit=False)
        comm.post = Post.objects.get(slug=self.kwargs.get("post_slug"))
        comm.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('single', kwargs={'cat_slug': self.kwargs.get("cat_slug"),
                                              'post_slug': self.kwargs.get("post_slug")})
