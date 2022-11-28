from django.contrib import admin
from .models import (
    Author, Category, Post, PostCategory, SubscribeCategory, Comment
)


class PostCategoryInLine(admin.TabularInline):
    model = PostCategory
    fk_name = 'postThrough'
    extra = 1


class PostAdmin(admin.ModelAdmin):
    inlines = [PostCategoryInLine]

    list_display = (
        'title', 'rating', 'dateCreation', 'categoryType', 'postAuthor',
    )
    list_filter = ('categoryType', 'postAuthor', 'postCategory', )
    search_fields = ('title', )


class PostCategoryAdmin(admin.ModelAdmin):
    list_display = ('postThrough', 'categoryThrough', )
    list_filter = ('categoryThrough', )


admin.site.register(Author)
admin.site.register(Category)
admin.site.register(Post, PostAdmin)
admin.site.register(PostCategory, PostCategoryAdmin)
admin.site.register(Comment)
admin.site.register(SubscribeCategory)
