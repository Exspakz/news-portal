from django.conf import settings
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.auth.models import AnonymousUser
from django.core.cache import cache
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views.generic import (
    TemplateView, ListView, DetailView, CreateView, UpdateView, DeleteView,
)

from datetime import datetime, timedelta

from .models import Author, Post, Category
from .forms import PostForm
from .filters import PostFilter
from .mixins import OwnerPermissionRequiredMixin


class PostList(ListView):
    model = Post
    ordering = '-dateCreation'
    template_name = 'news/posts.html'
    context_object_name = 'posts'
    paginate_by = 10


class PostDetail(DetailView):
    model = Post
    template_name = 'news/post.html'
    context_object_name = 'post'

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        context = self.get_context_data(object=self.object)
        return self.render_to_response(context)

    def get_object(self, *args, **kwargs):
        obj = cache.get(f'post-{self.kwargs["pk"]}', None)
        if not obj:
            obj = super().get_object(queryset=self.queryset)
            cache.set(f'post-{self.kwargs["pk"]}', obj)
        return obj

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        for category in self.get_object().postCategory.all():
            if not isinstance(self.request.user, AnonymousUser):
                context['is_subscriber'] = self.request.user.category_set.filter(pk=category.pk).exists()
        return context


class PostSearch(ListView):
    model = Post
    ordering = '-dateCreation'
    template_name = 'news/post_search.html'
    context_object_name = 'post_search'
    paginate_by = 5

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = PostFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context


class PostCreate(PermissionRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = 'news/post_create.html'
    permission_required = ('news.add_post', )

    def form_valid(self, form):
        self.object = form.save(commit=False)
        print(type(self.object))
        self.object.postAuthor = self.request.user.author
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data()

        limit = settings.DAILY_POST_LIMIT
        prev_day = datetime.utcnow() - timedelta(days=1)
        posts_day_count = Post.objects.filter(
            postAuthor__authorUser=self.request.user,
            dateCreation__gte=prev_day,
        ).count()
        context['count'] = posts_day_count
        context['limit'] = limit
        context['posts_limit'] = limit <= posts_day_count
        return context

    def get_success_url(self):
        return reverse('post_detail', kwargs={'pk': self.object.id})


class PostUpdate(OwnerPermissionRequiredMixin, UpdateView):
    model = Post
    form_class = PostForm
    template_name = 'news/post_update.html'
    permission_required = ('news.change_post', )

    def get_success_url(self):
        return reverse('post_detail', kwargs={'pk': self.kwargs['pk']})


class PostDelete(PermissionRequiredMixin, DeleteView):
    model = Post
    template_name = 'news/post_delete.html'
    context_object_name = 'post'
    success_url = reverse_lazy('post_list')
    permission_required = ('news.delete_post', )

    def get_success_url(self):
        return reverse('author_posts')


class PostAuthor(PermissionRequiredMixin, TemplateView):
    template_name = 'news/author_posts.html'
    permission_required = ('news.change_post', )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['author_posts'] = self.request.user.author.post_set.all
        return context


class CategoryList(ListView):
    model = Post
    template_name = 'news/category_list.html'
    context_object_name = 'categories'

    def get_queryset(self):
        self.postCategory = get_object_or_404(Category, id=self.kwargs['pk'])
        queryset = Post.objects.filter(postCategory=self.postCategory).order_by('-dateCreation')
        return queryset

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = self.postCategory
        return context
