from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum


class Author(models.Model):
    rating = models.SmallIntegerField(default=0)

    authorUser = models.OneToOneField(User, on_delete=models.CASCADE)

    def update_rating(self):
        post_rating = self.post_set.aggregate(Sum('rating')).get('rating__sum')

        comment_rating = self.authorUser.comment_set.aggregate(Sum('rating')).get('rating__sum')

        compost_rating = 0
        for i in self.post_set.all():
            compost_rating += i.comment_set.aggregate(Sum('rating')).get('rating__sum')

        self.rating = post_rating * 3 + comment_rating + compost_rating
        self.save()


class Category(models.Model):
    name = models.CharField(max_length=64, unique=True)


class Post(models.Model):
    NEWS = 'NW'
    ARTICLES = 'AR'
    CATEGORIES = [
        (NEWS, 'Новость'),
        (ARTICLES, 'Статья')
    ]

    title = models.CharField(max_length=128)
    text = models.TextField()
    rating = models.SmallIntegerField(default=0)
    dateCreation = models.DateTimeField(auto_now_add=True)
    categoryType = models.CharField(max_length=2, choices=CATEGORIES, default=ARTICLES)

    postAuthor = models.ForeignKey(Author, on_delete=models.CASCADE)
    postCategory = models.ManyToManyField(Category, through='PostCategory')

    def __str__(self):
        return f'{self.pk}: {self.title.title()}'

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()

    def preview(self):
        return f'{self.text[:124]}...'


class PostCategory(models.Model):
    postThrough = models.ForeignKey(Post, on_delete=models.CASCADE)
    categoryThrough = models.ForeignKey(Category, on_delete=models.CASCADE)


class Comment(models.Model):
    text = models.TextField()
    rating = models.SmallIntegerField(default=0)
    dateCreation = models.DateTimeField(auto_now_add=True)

    commentPost = models.ForeignKey(Post, on_delete=models.CASCADE)
    commentUser = models.ForeignKey(User, on_delete=models.CASCADE)

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()
