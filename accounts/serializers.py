from django.contrib.auth.models import User

from rest_framework import serializers

from .models import Profile, FriendRequest, FriendShip

class ProfileSerializer(serializers.ModelSerializer):
   class Meta:
      model = Profile
      fields = '__all__'
   
   def update(self, instance, validated_data):
      try:
         if not validated_data['image']:
            if instance.image: instance.image.delete()
         else:
            if instance.image: instance.image.delete()
      except KeyError:
         pass
      return super().update(instance, validated_data)

class UserSerializer(serializers.ModelSerializer):
   profile = serializers.SerializerMethodField()
   
   class Meta:
      model = User
      fields = ['username', 'email', 'id', 'password', 'profile']
      extra_kwargs = {'password': {'write_only': True,}}
   
   def get_profile(self, user):
      profile, created = Profile.objects.get_or_create(user=user)
      try:
         return ProfileSerializer(profile, context={'request': self.context['request']}).data
      except KeyError:
         return ProfileSerializer(profile).data

   def save(self, user):
      return print(user)

class RegisterSerializer(serializers.ModelSerializer):      
   class Meta:
      model = User
      fields = ['username', 'password', 'email', 'id']
      extra_kwargs = {'password': {'write_only': True,}}
   
   def create(self, validated_data):
      username = validated_data['username']
      email = validated_data['email']
      password = validated_data['password']
      user = User(username=username, email=email)
      user.set_password(password)
      user.save()
      return user

class UserData:
   def get_user_data(self, user):
      return UserSerializer(user).data

class FriendRequestSerializer(serializers.ModelSerializer, UserData):
   receiver_info = serializers.SerializerMethodField()
   sender_info = serializers.SerializerMethodField()

   class Meta:
      model = FriendRequest
      fields = "__all__"
   
   def get_receiver_info(self, obj):
      return self.get_user_data(obj.receiver)
   
   def get_sender_info(self, obj):
      return self.get_user_data(obj.sender)
   
   def create(self, validated_data):
      try:
        if validated_data['receiver'] == validated_data['sender']:
            raise serializers.ValidationError("friend request is not valid.", code=400) 
      except KeyError:
         pass
      
      return super().create(**validated_data)


class FriendShipSerializer(serializers.ModelSerializer, UserData):
   partener_info = serializers.SerializerMethodField()
   friend_info = serializers.SerializerMethodField()

   class Meta:
      model = FriendShip
      fields = "__all__"

   def get_friend_info(self, obj):
      return self.get_user_data(obj.friend)
   
   def get_partener_info(self, obj):
      return self.get_user_data(obj.partener)

   def create(self, validated_data):
      try:
        if validated_data['friend'] == validated_data['partener']:
            raise serializers.ValidationError("friendship is not valid.", code=400) 
      except KeyError:
         pass
      
      return super().create(**validated_data)
