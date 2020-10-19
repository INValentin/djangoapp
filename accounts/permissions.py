from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsHimself(BasePermission):

   def has_object_permission(self, request, view, obj):
      if not request.user.is_authenticated: return False
      if request.method in SAFE_METHODS:
         return True
      print("\n\n", request.user, obj, request.user == obj, sep="\n", end="\n\n")
      return request.user == obj

class InvolvedInFriendShip(BasePermission):

   def has_object_permission(self, request, view, obj):
      if not request.user.is_authenticated: return False
      if request.method in SAFE_METHODS:
         return True
      return request.user == obj.partener or request.user == obj.friend

class InvolvedInFriendRequest(BasePermission):

   def has_object_permission(self, request, view, obj):
      if not request.user.is_authenticated: return False
      return request.user == obj.sender or request.user == obj.receiver

