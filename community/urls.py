from django.urls import path
from . import views
urlpatterns = [
    path('movies/', views.MovieListPaginate.as_view()), # 모든 영화 조회하기
    path('movies/home/', views.MovieBest2.as_view()), # 영화 2개 보여주기
    path('movies/recommend/', views.MovieRecommend.as_view()), # 추천
    path('movies/<int:movie_pk>/', views.MovieDetail.as_view()), # 개별 영화 조회하기
    path('articles/', views.ArticleList.as_view()), # 모든 아티클 조회하기
    path('articles/home/', views.ArticleBest3.as_view()),
    path('articles/<int:pk>/', views.ArticleDetail.as_view()), # 개별 아티클 조회하기 및 생성하기
    path('articles/<int:pk>/comments/', views.CommentList.as_view()),# 댓글 작성하기, 삭제하기
    path('articles/<int:pk>/likes/', views.Like.as_view()),
]