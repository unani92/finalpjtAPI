from random import choice
from django.shortcuts import get_object_or_404
from django.db.models import Count
from rest_framework.response import Response
from rest_framework.decorators import permission_classes, APIView
from rest_framework.permissions import IsAuthenticated
from .serializers import MovieArticleSerializer, ArticleSerializer, ArticleListSerializer, CommentSerializer
from .models import Movie, Article, Comment
from rest_framework.generics import ListAPIView
from rest_framework.pagination import PageNumberPagination
from .rankcalculate import RankCalculate
# Create your views here.


# pagination config default class
class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_query_param = 'page'

# all movies, specific movie view
class MovieListPaginate(APIView):

    def get(self, request):
        paginator = StandardResultsSetPagination()
        if request.GET.get('orderBy'):
            orderBy = request.GET.get('orderBy')
            movies = Movie.objects.order_by(orderBy)
        elif request.GET.get('q'):
            q = request.GET.get('q')
            movies = Movie.objects.filter(title__icontains=q)
            serializer = MovieArticleSerializer(movies, many=True)
            return Response(serializer.data)
        else :
            return Response({"message": "no result"})

        result_page = paginator.paginate_queryset(movies,request)
        serializer = MovieArticleSerializer(result_page, many=True)
        return Response(serializer.data)

class MovieBest2(APIView):
    def get(self, request):
        movies = Movie.objects.order_by('-popularity')[:2]
        serializer = MovieArticleSerializer(movies, many=True)
        return Response(serializer.data)

class MovieDetail(APIView):
    def get(self, request, movie_pk):
        movie = get_object_or_404(Movie, pk=movie_pk)
        serializer = MovieArticleSerializer(movie)
        return Response(serializer.data)

class MovieRecommend(APIView):
    @permission_classes([IsAuthenticated])
    def get(self, request):
        if request.user.articles.all():
            gnr_cnt = dict()
            articles = request.user.articles.all()
            for article in articles:
                movie = article.movie
                genres = movie.genres.all()
                for genre in genres:
                    gnr_cnt[genre.pk] = gnr_cnt.get(genre.pk, 0) + 1
            fav_gnr = sorted(gnr_cnt.items(), key=lambda x:x[1], reverse=True)[0][0]
            movies = list(Movie.objects.filter(genres=fav_gnr).all())
        else:
            movies = list(Movie.objects.filter(vote_average__gte=8).all())
        movie = choice(movies)
        serializer = MovieArticleSerializer(movie)
        return Response(serializer.data)

# all articles, specific article CRUD
class ArticleList(APIView):
    def get(self,request):
        articles = Article.objects.order_by('-pk')
        serializer = ArticleListSerializer(articles, many=True)
        return Response(serializer.data)

class ArticleBest3(APIView):
    def get(self,request):
        articles = Article.objects.annotate(count=Count('like_users')).order_by('-count')[:3]
        serializer = ArticleListSerializer(articles, many=True)
        return Response(serializer.data)


class ArticleDetail(APIView):
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

            new_rank = RankCalculate(movie,request)
            new_rank.AddNewRank()

            return Response(serializer.data)
        else:
            print(serializer.data)
            return Response({"msg": "error"})

    @permission_classes([IsAuthenticated])
    def put(self, request, pk):
        article = get_object_or_404(Article, pk=pk)

        if request.user.username == article.user.username:
            prev_rank = article.rank
            serializer = ArticleSerializer(article, data=request.data)
            if serializer.is_valid(raise_exception=True):
                serializer.save()

                new_rank = RankCalculate(article,request)
                new_rank.UpdateNewRank(prev_rank)

                return Response(serializer.data)
            else :
                return Response({"msg":"error"})
        else :
            return Response({
                "msg":"401 unAuthorized 잘못된 접근입니다.",
                "articleUser": article.user.username,
                "requestUser": request.user.username
            })

    @permission_classes([IsAuthenticated])
    def delete(self, request, pk):
        article = get_object_or_404(Article, pk=pk)

        if request.user == article.user:
            prev_rank = article.rank

            new_rank = RankCalculate(article,request)
            new_rank.DeleteRank(prev_rank)

            article.delete()
            return Response({"msg":"deleted"})
        else :
            return Response({"msg": "401 unAuthorized 잘못된 접근입니다."})

# all comments, specific comment CRD
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
        if request.user == comment.user:
            comment.delete()
            return Response({"msg":"deleted"})
        else :
            return Response({"msg": "401 unAuthorized 잘못된 접근입니다."})

class Like(APIView):
    def get(self, request, pk):
        user = request.user
        article = get_object_or_404(Article, pk=pk)

        if user in article.like_users.all():
            article.like_users.remove(user)
            liked = False
        else :
            article.like_users.add(user)
            liked = True

        return Response({
            "liked": liked,
            "count": article.like_users.count()
        })

