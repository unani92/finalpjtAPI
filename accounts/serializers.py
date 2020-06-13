from rest_framework import serializers
from django.contrib.auth import get_user_model
from community.models import Article, Movie
User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id','username','age']

class MovieSerializer(serializers.ModelSerializer):
    # genres = GenreSerializer(many=True)
    class Meta:
        model = Movie
        fields = ['id', 'genres', 'title', 'overview', 'poster_path', 'release_date', 'popularity', 'vote_count', 'vote_average', 'adult']

class ArticleSerializer(serializers.ModelSerializer):
    movie = MovieSerializer()
    class Meta:
        model = Article
        fields = ['id', 'movie', 'title', 'content', 'updated_at']

class UserArticleSerializer(UserSerializer):
    articles = ArticleSerializer(many=True)
    like_articles = ArticleSerializer(many=True)
    class Meta(UserSerializer.Meta):
        fields = UserSerializer.Meta.fields + ['articles', 'like_articles']

