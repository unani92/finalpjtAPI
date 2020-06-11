from rest_framework import serializers
from .models import Movie, Genre, Article, Comment
from accounts.serializers import UserSerializer

class GenreSerializer(serializers.Serializer):
    class Meta:
        model = Genre
        fields = ['name']

class MovieSerializer(serializers.Serializer):
    genres = GenreSerializer(many=True)
    class Meta(GenreSerializer.Meta):
        model = Movie
        fields = ['genres', 'title', 'overview', 'poster_path', 'release_date', 'popularity', 'vote_count', 'vote_average', 'adult']

class CommentSerializer(serializers.Serializer):
    user = UserSerializer(required=False)
    class Meta:
        model = Comment
        fields = ['id', 'content', 'created_at', ]

class ArticleListSerializer(serializers.Serializer):
    user = UserSerializer()
    movie = MovieSerializer()
    like_users = UserSerializer(many=True)
    class Meta:
        model = Article
        fields = '__all__'

class ArticleSerializer(serializers.Serializer):
    user = UserSerializer(required=False)
    movie = MovieSerializer(required=False)
    like_users = UserSerializer(many=True)
    class Meta:
        model = Article
        fields = '__all__'
