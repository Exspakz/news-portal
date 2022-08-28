from django import forms

from .models import Author, Category, Post, PostCategory


class PostForm(forms.ModelForm):
    postAuthor = forms.ModelChoiceField(
        label='Author',
        empty_label='Select a author',
        queryset=Author.objects.all(),
    )

    postCategory = forms.ModelMultipleChoiceField(
        label='Category',
        queryset=Category.objects.all(),
    )

    categoryType = forms.ChoiceField(label='Type', choices=Post.CATEGORIES)

    class Meta:
        model = Post
        fields = [
            'title',
            'text',
            'postAuthor',
            'postCategory',
            'categoryType',
        ]
