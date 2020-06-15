from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.conf import settings
# Create your models here.

class Genre(models.Model):
    name = models.CharField(max_length=200)

class Movie(models.Model):
    genres = models.ManyToManyField(
        Genre,
        related_name='movies'
    )
    title = models.CharField(max_length=200)
    overview = models.TextField()
    poster_path = models.URLField(null=True)
    release_date = models.DateField()
    popularity = models.FloatField()
    vote_count = models.IntegerField()
    vote_average = models.FloatField()
    adult = models.BooleanField()

class Article(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    rank = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(10)]
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='articles',
        on_delete=models.CASCADE
    )
    movie = models.ForeignKey(
        Movie,
        related_name='articles',
        on_delete=models.CASCADE
    )
    like_users = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name='like_articles',
    )

class Comment(models.Model):
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    article = models.ForeignKey(
        Article,
        related_name='comments',
        on_delete=models.CASCADE
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='comments',
        on_delete=models.CASCADE
    )

