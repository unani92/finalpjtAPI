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
        fields = ['id', 'genres', 'title', 'overview', 'poster_path', 'release_date', 'popularity', 'vote_count', 'vote_average', 'adult']

class ArticleListSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    movie = MovieSerializer()
    like_users = UserSerializer(many=True)
    class Meta:
        model = Article
        fields = '__all__'

# 게시글 작성용
class ArticleSerializer(serializers.ModelSerializer):
    user = UserSerializer(required=False)
    movie = MovieSerializer(required=False)
    class Meta:
        model = Article
        fields = ['movie', 'user', 'title', 'content', 'rank', ]

# 영화정보 및 영화에 달린 게시글
class ArticleRelatedMovieSerializer(serializers.ModelSerializer):
    user = UserSerializer(required=False)
    class Meta:
        model = Article
        fields = ['id' ,'user', 'title', 'content', 'rank', 'created_at', 'updated_at']

class MovieArticleSerializer(MovieSerializer):
    articles = ArticleRelatedMovieSerializer(many=True)
    class Meta(MovieSerializer.Meta):
        fields = MovieSerializer.Meta.fields + ['articles']

class CommentSerializer(serializers.Serializer):
    user = UserSerializer(required=False)
    class Meta:
        model = Comment
        fields = ['id', 'content', 'created_at', ]