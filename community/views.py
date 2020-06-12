from django.shortcuts import render, get_object_or_404
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from .serializers import MovieArticleSerializer, GenreSerializer, ArticleSerializer, ArticleListSerializer, CommentSerializer
from .models import Movie, Genre, Article
# Create your views here.

@api_view(['GET'])
def index(request):
    movies = Movie.objects.all()
    serializer = MovieArticleSerializer(movies,many=True)
    return Response(serializer.data)

@api_view(['GET'])
def movie_best3(request):
    movies = Movie.objects.order_by('-vote_average')[:3]
    serializer = MovieArticleSerializer(movies,many=True)
    return Response(serializer.data)

@api_view(['GET'])
def moviedetail(request,movie_pk):
    movie = get_object_or_404(Movie, pk=movie_pk)
    serializer = MovieArticleSerializer(movie)
    return Response(serializer.data)

# 게시글 작성 및 조회하기
@api_view(['POST','GET'])
@permission_classes([IsAuthenticated])
def article_view_create(request,pk):
    if request.method == 'POST':
        movie = get_object_or_404(Movie, pk=pk)
        serializer = ArticleSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(user=request.user, movie=movie)
            return Response(serializer.data)
        else :
            print(serializer.data)
            return Response({"msg":"error"})
    else :
        article = get_object_or_404(Article, pk=pk)
        serializer = ArticleListSerializer(article)
        return Response(serializer.data)

# 댓글 작성하기
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def comment_create(request,article_pk):
    article = get_object_or_404(Article, pk=article_pk)
    serializer = CommentSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
        serializer.save(user=request.user, article=article)
        return Response(serializer.data)
