import django_filters

from django.forms import DateInput
from django_filters import FilterSet
from .models import Author, Post, Category


class PostFilter(FilterSet):
    title = django_filters.CharFilter(
        field_name='title',
        lookup_expr='icontains',
        label='Title',
    )

    dateCreation = django_filters.DateTimeFilter(
        field_name='dateCreation',
        lookup_expr='gt',
        label='Date',
        widget=DateInput(
            format='%Y-%m-%d',
            attrs={'type': 'date'},
        ),
    )

    author = django_filters.ModelChoiceFilter(
        field_name='postAuthor',
        queryset=Author.objects.all(),
        label='Author',
        empty_label='Select a author',
    )

    category = django_filters.ModelChoiceFilter(
        field_name='postCategory',
        queryset=Category.objects.all(),
        label='Category',
        empty_label='Select a category',
    )

    type = django_filters.ChoiceFilter(
        field_name='categoryType',
        label='Type',
        empty_label='Select a type',
        choices=Post.CATEGORIES,
    )

    # class Meta:
    #     model = Post
    #     fields = [
    #         'title',
    #         'dateCreation',
    #         'categoryType',
    #         'postAuthor',
    #         'postCategory',
    #     ]
