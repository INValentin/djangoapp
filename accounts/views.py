from django.shortcuts import render
from django.contrib.auth.models import User
from django.http.response import JsonResponse
from django.contrib.auth.forms import UserCreationForm
from django.db.models import Q

from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticatedOrReadOnly, AllowAny, IsAuthenticated
from rest_framework.generics import RetrieveAPIView, CreateAPIView, RetrieveDestroyAPIView
from rest_framework.decorators import action
from rest_framework.response import Response

from posts.mixins import ChildList
from posts.serializers import PostSerializer, BaseNotificationSerializer
from posts.models import BaseNotification

from .models import Profile, FriendRequest, FriendShip
from .permissions import IsHimself, InvolvedInFriendRequest, InvolvedInFriendShip
from .serializers import (
   UserSerializer, RegisterSerializer, ProfileSerializer, FriendRequestSerializer, FriendShipSerializer
)

# Create your views here.

class RegisterUserView(CreateAPIView):
   serializer_class = RegisterSerializer
   permission_classes = [AllowAny]
   

class CurrentUserView(RetrieveAPIView):
   serializer_class = UserSerializer
   queryset = User.objects.all()
   permission_classes = [IsAuthenticated,]

   def get_object(self):
      return self.request.user

class RetrieveDeleteNotification(RetrieveDestroyAPIView):
   serializer_class = BaseNotificationSerializer
   queryset = BaseNotification.objects.all()
   permission_classes = [IsAuthenticated]

   def delete(self, request, pk, **kwargs):
      notification = self.get_object()
      if request.user in notification.recievers.all():
         if notification.recievers.count() == 1:
            return self.destroy(request, pk, **kwargs)
         notification.recievers.remove(request.user)
         return Response({}, status=204)
      return Response({'Forbidden': "can't delete notification"}, status=403)


class ReadNotification(CreateAPIView):
   permission_classes = [IsAuthenticated,]

   def post(self, request, pk, *args, **kwargs):
      try:
         notification = BaseNotification.objects.get(pk=pk)
         notification.seen_by.add(request.user)
      except BaseNotification.DoesNotExist:
         pass

      return Response({}, status=201)


class ReadAllNotifications(CreateAPIView):
   permission_classes = [IsAuthenticated,]
   serializer_class = BaseNotificationSerializer

   def post(self, request, *args, **kwargs):
      for notification in request.user.notifications.all():
         notification.seen_by.add(request.user) 

      return Response({}, status=201)


class UserViewSet(ModelViewSet, ChildList):
   queryset = User.objects.all()
   serializer_class = UserSerializer
   child_serializer = PostSerializer
   permission_classes = [IsAuthenticated, IsHimself]

   @action(detail=True, methods=['GET', 'POST'])
   def profile(self, request, pk=None):
      user = User.objects.get(pk=pk)
      profile, created = Profile.objects.get_or_create(user=user)

      if request.method == 'GET':
         serializer = ProfileSerializer(profile, context={'request': request})
         return Response(serializer.data)

      serializer = ProfileSerializer(profile, data=request.data, context={'request': request})
      serializer.is_valid(raise_exception=True)
      serializer.save(user=user)
      return Response(serializer.data)

   @action(detail=False, methods=['GET'], permission_classes=[IsAuthenticated,])
   def unread_notifications(self, request, *args, **kwargs):
      user = request.user
      q = user.notifications.all()
      queryset = q.exclude(seen_by__username__exact=request.user.username)

      page = self.paginate_queryset(queryset)
      serializer = BaseNotificationSerializer(page, many=True, context={'request': request})
   
      data = serializer.data

      for notification in data:
         n = dict(notification)
         if not n['obj'] or (n['on_model'] and not n['on_obj']):
            del data[data.index(notification)]
      
      return self.get_paginated_response(data)
   
   @action(detail=True, methods=['GET',])
   def notifications(self, request, pk):
      user = self.get_object()
      
      queryset = user.notifications.all()
      
      for notification in queryset:
         notification.__setattr__('is_read', user in notification.seen_by.all())
         
      page = self.paginate_queryset(queryset)
      serializer = BaseNotificationSerializer(page, many=True, context={'request': request})
      
      data = serializer.data

      for notification in data:
         n = dict(notification)
         if not n['obj'] or (n['on_model'] and not n['on_obj']):
            del data[data.index(notification)]

      return self.get_paginated_response(data)

   @action(detail=True, methods=['GET',])
   def posts(self, request, pk=None):
      return super().list_child(request, pk)

   @action(detail=True, methods=['POST', 'GET'])
   def friends(self, request, pk):
      user = self.get_object()
      queryset = FriendShip.objects.filter(Q(friend=user) | Q(partener=user))
      page = self.paginate_queryset(queryset)

      serializer = FriendShipSerializer(page, many=True, context={'request': request})
      
      return self.get_paginated_response(serializer.data)

   def perform_destroy(self, instance): 
      if instance.profile.image:
         instance.profile.image.delete()
      return super().perform_destroy(instance)

   get_child_queryset = lambda self, user: user.posts.all()


class FriendShipViewSet(ModelViewSet):
   serializer_class = FriendShipSerializer
   queryset = FriendShip.objects.all()
   permission_classes = [IsAuthenticated, InvolvedInFriendShip]
   

class FriendRequestViewSet(ModelViewSet):
   serializer_class = FriendRequestSerializer
   queryset = FriendRequest.objects.all()
   permission_classes = [IsAuthenticated, InvolvedInFriendRequest]