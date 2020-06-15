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


# 게시글 작성용
class ArticleSerializer(serializers.ModelSerializer):
    user = UserSerializer(required=False)
    movie = MovieSerializer(required=False)
    class Meta:
        model = Article
        fields = ['id','movie', 'user', 'title', 'content', 'rank', ]

# 영화정보 및 영화에 달린 게시글
class ArticleRelatedMovieSerializer(serializers.ModelSerializer):
    user = UserSerializer(required=False)
    class Meta:
        model = Article
        fields = ['id' ,'user', 'title', 'content', 'rank', 'updated_at']



# 댓글 작성
class CommentSerializer(serializers.ModelSerializer):
    user = UserSerializer(required=False)
    article = ArticleRelatedMovieSerializer(required=False)
    class Meta:
        model = Comment
        fields = ['id', 'article', 'user', 'content', 'created_at', ]

class CommentsRelatedArticleSerializer(serializers.ModelSerializer):
    user = UserSerializer(required=False)
    class Meta:
        model = Comment
        fields = ['id', 'user', 'content', 'created_at', ]

# 개별 게시글 조회하기
class MovieRelatedArticleSerializer(serializers.ModelSerializer):
    genres = GenreSerializer(many=True)
    class Meta:
        model = Movie
        fields = ['id', 'genres', 'title', 'popularity', 'vote_count', 'vote_average', 'adult']

class ArticleListSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    movie = MovieRelatedArticleSerializer()
    comments = CommentsRelatedArticleSerializer(many=True)
    like_users = UserSerializer(many=True)
    class Meta:
        model = Article
        fields = ['id', 'movie', 'user', 'title', 'content', 'rank', 'created_at', 'updated_at', 'like_users', 'comments']

# 모든 영화 조회하기
class MovieArticleSerializer(MovieSerializer):
    articles = ArticleListSerializer(many=True)
    class Meta(MovieSerializer.Meta):
        fields = MovieSerializer.Meta.fields + ['articles']
