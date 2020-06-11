from django.urls import path
from . import views
urlpatterns = [
    path('movies/', views.index),
    path('movies/<int:movie_pk>/', views.moviedetail),
    path('articles/<int:movie_pk>/', views.article_create),

]