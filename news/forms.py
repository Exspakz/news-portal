from django import forms
from django.core.exceptions import ValidationError

from .models import Author, Category, Post


class PostForm(forms.ModelForm):
    text = forms.CharField(min_length=500)

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
            'categoryType',
            'postCategory',
        ]

    def clean(self):
        cleaned_data = super().clean()
        title = cleaned_data.get('title')
        if title[0].islower():
            raise ValidationError({
                'title': 'The title should start with uppercase letter'
            })

        return cleaned_data
