from django.conf import settings
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.auth.models import AnonymousUser
from django.urls import reverse_lazy
from django.views.generic import (
    TemplateView, ListView, DetailView, CreateView, UpdateView, DeleteView,
)

from datetime import datetime, timedelta

from .models import Author, Post
from .forms import PostForm
from .filters import PostFilter
from .mixins import OwnerPermissionRequiredMixin


class PostList(ListView):
    model = Post
    ordering = 'dateCreation'
    template_name = 'news/posts.html'
    context_object_name = 'posts'
    paginate_by = 5


class PostDetail(DetailView):
    model = Post
    template_name = 'news/post.html'
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        for category in self.get_object().postCategory.all():
            if not isinstance(self.request.user, AnonymousUser):
                context['is_subscriber'] = self.request.user.category_set.filter(pk=category.pk).exists()
        return context


class PostSearch(ListView):
    model = Post
    template_name = 'news/post_search.html'
    context_object_name = 'post_search'

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
        self.object.postAuthor = Author.objects.get(authorUser=self.request.user)
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


class PostUpdate(OwnerPermissionRequiredMixin, UpdateView):
    model = Post
    form_class = PostForm
    template_name = 'news/post_update.html'
    permission_required = ('news.change_post', )


class PostDelete(PermissionRequiredMixin, DeleteView):
    model = Post
    template_name = 'news/post_delete.html'
    success_url = reverse_lazy('post_list')
    permission_required = ('news.delete_post', )


class PostAuthor(PermissionRequiredMixin, TemplateView):
    template_name = 'news/author_posts.html'
    permission_required = ('news.change_post', )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['author_posts'] = self.request.user.author.post_set.all
        return context
