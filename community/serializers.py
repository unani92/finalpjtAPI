from rest_framework import serializers
from .models import Movie, Genre, Article, Comment
from accounts.serializers import UserSerializer

class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = '__all__'

class MovieSerializer(serializers.ModelSerializer):
    genres = GenreSerializer(many=True)
    class Meta:
        model = Movie
        fields = ['genres', 'title', 'overview', 'poster_path', 'release_date', 'popularity', 'vote_count', 'vote_average', 'adult']

class CommentSerializer(serializers.Serializer):
    user = UserSerializer(required=False)
    class Meta:
        model = Comment
        fields = ['id', 'content', 'created_at', ]

class ArticleListSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    movie = MovieSerializer()
    like_users = UserSerializer(many=True)
    class Meta:
        model = Article
        fields = '__all__'

class ArticleSerializer(serializers.ModelSerializer):
    user = UserSerializer(required=False)
    movie = MovieSerializer(required=False)
    class Meta:
        model = Article
        fields = ['title', 'content', 'rank', 'user', 'movie']

class MovieArticleSerializer(MovieSerializer):
    articles = ArticleSerializer(many=True)
    class Meta(MovieSerializer.Meta):
        fields = MovieSerializer.Meta.fields + ['articles']
