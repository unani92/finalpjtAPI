from django.urls import path
from . import views
urlpatterns = [
    path('movies/', views.index), # 모든 영화 조회하기
    path('movies/<int:movie_pk>/', views.moviedetail), # 개별 영화 조회하기
    path('articles/<int:pk>/', views.article_view_create), # 개별 아티클 조회하기 및 생성하기
    path('comments/<int:article_pk>/', views.comment_create) # 댓글 작성하기
]