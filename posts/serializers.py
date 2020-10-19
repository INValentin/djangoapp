from rest_framework import serializers
from django.contrib.auth.models import User

from .models import Post, Comment, Reply, BaseNotification

from accounts.serializers import UserSerializer

class UserInfo:
   def get_user_info(self, obj):
      return UserSerializer(obj.user, context=self.context).data

   def get_likes_count(self, obj):
      return obj.likes.count()

class ReplySerializer(serializers.ModelSerializer, UserInfo):
   user_info = serializers.SerializerMethodField()
   likes_count = serializers.SerializerMethodField()

   class Meta:
      model = Reply
      exclude = ('user',)

class CommentSerializer(serializers.ModelSerializer, UserInfo):
   user_info = serializers.SerializerMethodField()
   likes_count = serializers.SerializerMethodField()
   replies = serializers.SerializerMethodField()

   class Meta:
      model = Comment
      exclude = ('user',)
   
   def get_replies(self, obj):
      return obj.replies.count()

class PostSerializer(serializers.ModelSerializer, UserInfo):
   user_info = serializers.SerializerMethodField()
   likes_count = serializers.SerializerMethodField()
   comments = serializers.SerializerMethodField()

   class Meta:
      model = Post
      exclude = ('user',)
   
   def get_comments(self, obj):
      return obj.comments.count()

   
   def update(self, instance, validated_data):
      try:
         if not validated_data['image']:
            if instance.image: instance.image.delete()
         else:
            if instance.image: instance.image.delete()
               
      except KeyError:
         pass
   
      return super().update(instance, validated_data)

class LikeSerializer(serializers.Serializer):
   users = serializers.SerializerMethodField()
   likes_count = serializers.SerializerMethodField()
   
   def get_likes_count(self, obj):
      return obj.likes.count()

   def get_users(self, obj):
      return [UserSerializer(user).data for user in obj.likes.all()]


class BaseNotificationSerializer(serializers.ModelSerializer):
   obj = serializers.SerializerMethodField()
   on_obj = serializers.SerializerMethodField()
   on_obj_owner = UserSerializer()
   user = UserSerializer()
   
   class Meta:
      model = BaseNotification
      exclude = ['recievers', 'seen_by']

   def get_on_obj(self, obj):
      return self.use_obj(model_name=obj.on_model, obj_id=obj.on_obj_id, pk=obj.id)

   def get_obj(self, obj):
      return self.use_obj(model_name=obj.model, obj_id=obj.obj_id, pk=obj.id)
   
   def get_data(self, model, serializer, obj_id, pk):
      try:
         return serializer(model.objects.get(pk=obj_id), context=self.context).data
      except model.DoesNotExist:
         try:
            obj = BaseNotification.objects.get(pk=pk).delete()
         except BaseNotification.DoesNotExist:
            return None
   
   def use_obj(self, model_name, obj_id, pk):
      if model_name == 'Post':
         return self.get_data(model=Post, serializer=PostSerializer, obj_id=obj_id, pk=pk)
      elif model_name == 'Comment':
         return self.get_data( model=Comment, serializer=CommentSerializer, obj_id=obj_id, pk=pk)
      elif model_name == 'Reply':
         return self.get_data(model=Reply, serializer=ReplySerializer, obj_id=obj_id, pk=pk)
      else:
         return None