from django.shortcuts import render, get_object_or_404
from rest_framework.response import Response
from rest_framework.decorators import permission_classes, APIView
from rest_framework.permissions import IsAuthenticated
from .serializers import UserArticleSerializer
from django.contrib.auth import get_user_model
# Create your views here.

User = get_user_model()
class UserArticleList(APIView):
    @permission_classes([IsAuthenticated])
    def get(self, request):
        user = User.objects.all()
        serializers = UserArticleSerializer(user, many=True)
        return Response(serializers.data)

class UserArticleDetail(APIView):
    @permission_classes([IsAuthenticated])
    def get(self, request, pk):
        user = get_object_or_404(User, pk=pk)
        serializers = UserArticleSerializer(user)
        return Response(serializers.data)

class RequestUserDetail(APIView):
    @permission_classes([IsAuthenticated])
    def get(self,request):
        user = request.user
        serializer = UserArticleSerializer(user)
        return Response(serializer.data)
