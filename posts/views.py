from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.http.response import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAuthenticatedOrReadOnly
from rest_framework.pagination import PageNumberPagination
from rest_framework.generics import RetrieveAPIView

from . import serializers
from .mixins import ChildList, LikeAction
from .models import Post, Comment, Reply
from .permissions import IsCommentOwner, IsOwner, IsPostOwner

# Create your views here.

class PostViewSet(ModelViewSet, LikeAction, ChildList):
   permission_classes = [IsOwner, IsAuthenticated]
   queryset = Post.objects.all()
   serializer_class = serializers.PostSerializer
   child_serializer = serializers.CommentSerializer

   @action(detail=True)
   def comments(self, request, pk=None):
      return super().list_child(request, pk)
   
   get_child_queryset = lambda self, post: post.comments.all()

   def perform_create(self, serializer):
      serializer.save(user=self.request.user)

   def perform_destroy(self, post):
      if post.image:
         post.image.delete()
      post.delete()

class CommentViewSet(ModelViewSet, LikeAction, ChildList):
   permission_classes = [IsOwner | IsPostOwner, IsAuthenticated]
   queryset = Comment.objects.all()
   serializer_class = serializers.CommentSerializer
   child_serializer = serializers.ReplySerializer
   
   def perform_create(self, serializer):
      serializer.save(user=self.request.user)

   @action(detail=True)
   def replies(self, request, pk=None):
      return super().list_child(request, pk)
   
   get_child_queryset = lambda self, comment: comment.replies.all()

class ReplyViewSet(ModelViewSet, LikeAction):
   permission_classes = [IsOwner | IsCommentOwner, IsAuthenticated]
   queryset = Reply.objects.all()
   serializer_class = serializers.ReplySerializer

   def perform_create(self, serializer):
      serializer.save(user=self.request.user)

