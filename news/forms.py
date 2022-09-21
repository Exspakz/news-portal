from django import forms
from django.core.exceptions import ValidationError

from .models import Category, Post


class PostForm(forms.ModelForm):
    title = forms.CharField(max_length=128)
    text = forms.CharField(min_length=300, widget=forms.Textarea)

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
