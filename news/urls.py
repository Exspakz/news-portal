from django.urls import path

from .views import (
    PostList, PostDetail, PostSearch, PostCreate, PostUpdate, PostDelete, PostAuthor, CategoryList,
)

urlpatterns = [
    path('', PostList.as_view(), name='post_list'),
    path('<int:pk>', PostDetail.as_view(), name='post_detail'),
    path('search/', PostSearch.as_view(), name='post_search'),
    path('create/', PostCreate.as_view(), name='post_create'),
    path('<int:pk>/update/', PostUpdate.as_view(), name='post_update'),
    path('<int:pk>/delete/', PostDelete.as_view(), name='post_delete'),
    path('author/', PostAuthor.as_view(), name='author_posts'),
    path('categories/<int:pk>', CategoryList.as_view(), name='category_list'),
]
