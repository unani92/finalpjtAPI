from django.shortcuts import render, get_object_or_404
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes, APIView
from rest_framework.permissions import IsAuthenticated
from .serializers import MovieArticleSerializer, GenreSerializer, ArticleSerializer, ArticleListSerializer, CommentSerializer
from .models import Movie, Genre, Article
# Create your views here.

class MovieList(APIView):
    def get(self, request):
        movies = Movie.objects.all()
        serializer = MovieArticleSerializer(movies,many=True)
        return Response(serializer.data)

class MovieBest3(APIView):
    def get(self, request):
        movies = Movie.objects.order_by('-popularity')[:3]
        serializer = MovieArticleSerializer(movies, many=True)
        return Response(serializer.data)

class MovieDetail(APIView):
    def get(self, request, movie_pk):
        movie = get_object_or_404(Movie, pk=movie_pk)
        serializer = MovieArticleSerializer(movie)
        return Response(serializer.data)

class ArticleList(APIView):
    @permission_classes([IsAuthenticated])
    def post(self, request, pk):
        movie = get_object_or_404(Movie, pk=pk)
        serializer = ArticleSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(user=request.user, movie=movie)
            return Response(serializer.data)
        else:
            print(serializer.data)
            return Response({"msg": "error"})

    def get(self, request, pk):
        article = get_object_or_404(Article, pk=pk)
        serializer = ArticleListSerializer(article)
        return Response(serializer.data)

class CommentList(APIView):
    @permission_classes([IsAuthenticated])
    def post(self, request, article_pk):
        article = get_object_or_404(Article, pk=article_pk)
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(user=request.user, article=article)
            return Response(serializer.data)
