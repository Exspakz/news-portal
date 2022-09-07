from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views.generic import (
    TemplateView, ListView, DetailView, CreateView, UpdateView, DeleteView,
)

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


class PostCreate(OwnerPermissionRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = 'news/post_create.html'
    permission_required = ('news.add_post', )

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.postAuthor = Author.objects.get(authorUser=self.request.user)
        return super().form_valid(form)


class PostUpdate(OwnerPermissionRequiredMixin, UpdateView):
    model = Post
    form_class = PostForm
    template_name = 'news/post_update.html'
    success_url = reverse_lazy('post_detail')
    permission_required = ('news.change_post', )


class PostDelete(PermissionRequiredMixin, DeleteView):
    model = Post
    template_name = 'news/post_delete.html'
    success_url = reverse_lazy('post_list')
    permission_required = ('news.delete_post', )


class PostAuthor(PermissionRequiredMixin, TemplateView):
    template_name = 'news/post_author.html'
    permission_required = ('news.change_post', )
