from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.decorators import permission_classes, APIView
from rest_framework.permissions import IsAuthenticated
from .serializers import MovieArticleSerializer, ArticleSerializer, ArticleListSerializer, CommentSerializer
from .models import Movie, Article, Comment
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
    def get(self, request, pk):
        article = get_object_or_404(Article, pk=pk)
        serializer = ArticleListSerializer(article)
        return Response(serializer.data)

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

    @permission_classes([IsAuthenticated])
    def put(self, request, pk):
        article = get_object_or_404(Article, pk=pk)
        serializer = ArticleSerializer(article, data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)
        else :
            return Response({"msg":"error"})

    @permission_classes([IsAuthenticated])
    def delete(self, request, pk):
        article = get_object_or_404(Article, pk=pk)
        article.delete()
        return Response({"msg":"deleted"})

class CommentList(APIView):
    def get(self, request, pk):
        comment = get_object_or_404(Comment, pk=pk)
        serializer = CommentSerializer(comment)
        return Response(serializer.data)

    @permission_classes([IsAuthenticated])
    def post(self, request, pk):
        article = get_object_or_404(Article, pk=pk)
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(user=request.user, article=article)
            return Response(serializer.data)

    @permission_classes([IsAuthenticated])
    def delete(self, request, pk):
        comment = get_object_or_404(Comment, pk=pk)
        comment.delete()
        return Response({"msg":"deleted"})