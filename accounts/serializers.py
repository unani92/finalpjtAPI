from rest_framework import serializers
from django.contrib.auth import get_user_model
from community.models import Article, Movie, Genre, Comment
User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id','username','age']

class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = '__all__'

class MovieRelatedArticleSerializer(serializers.ModelSerializer):
    genres = GenreSerializer(many=True)
    class Meta:
        model = Movie
        fields = ['id', 'genres', 'title', 'popularity', 'vote_count', 'vote_average', 'adult']

class CommentsRelatedArticleSerializer(serializers.ModelSerializer):
    user = UserSerializer(required=False)
    class Meta:
        model = Comment
        fields = ['id', 'user', 'content', 'created_at', ]

class ArticleListSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    movie = MovieRelatedArticleSerializer()
    comments = CommentsRelatedArticleSerializer(many=True)
    like_users = UserSerializer(many=True)
    class Meta:
        model = Article
        fields = ['id', 'movie', 'user', 'title', 'content', 'rank', 'created_at', 'updated_at', 'like_users', 'comments']


class UserArticleSerializer(UserSerializer):
    articles = ArticleListSerializer(many=True)
    like_articles = ArticleListSerializer(many=True)
    comments = CommentsRelatedArticleSerializer(many=True)
    class Meta(UserSerializer.Meta):
        fields = UserSerializer.Meta.fields + ['articles', 'like_articles', 'comments']

