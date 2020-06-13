from django.urls import path
from . import views

urlpatterns = [
    path('', views.UserArticleList.as_view()),
    path('<int:pk>/', views.UserArticleDetail.as_view())
]