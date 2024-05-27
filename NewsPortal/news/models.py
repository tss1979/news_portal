from django.db import models
from django.contrib.auth.models import User

KIND = ['N', 'A']

KIND_DICT = {'N': 'Новости', 'A': 'Статья'}


class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    rating = models.IntegerField(default=0)

    def update_rating(self):
        rating_posts = [int(x.get('rating')) for x in Post.objects.filter(author=self.pk).values('rating')]
        rating_comments = [int(x.get('rating')) for x in Comment.objects.filter(user=self.pk).values('rating')]
        rating_posts_comments = [int(x.get('rating')) for x in Comment.objects.filter(post__author=1).values('rating')]
        self.rating = sum(rating_posts) * 3 + sum(rating_comments) + sum(rating_posts_comments)
        self.save()
        return self.rating


class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)


class Post(models.Model):
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    post_kind = models.CharField(max_length=1, choices=KIND_DICT)
    created_at = models.DateTimeField(auto_now_add=True)
    category = models.ManyToManyField(Category, through="PostCategory")
    title = models.TextField()
    text = models.TextField
    rating = models.IntegerField(default=0)

    def like(self):
        self.rating += 1

    def dislike(self):
        self.rating += -1

    def preview(self):
        return self.text[:124] + '...'


class PostCategory(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    text = models.TextField
    rating = models.IntegerField(default=0)

    def like(self):
        self.rating += 1

    def dislike(self):
        self.rating += -1

