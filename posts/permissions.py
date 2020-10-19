from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsOwner(BasePermission):
   '''
      Check if the authenticated user is the owner of the object
   '''

   def has_object_permission(self, request, view, obj):
      if not request.user.is_authenticated:
         return False 

      if request.method in SAFE_METHODS: return True
      return request.user == obj.user

class IsPostOwner(BasePermission):
   def has_object_permission(self, request, view, comment):
      if not request.user.is_authenticated:
         return False

      if request.method in SAFE_METHODS: return True
      return request.user == comment.post.user

class IsCommentOwner(BasePermission):

   def has_object_permission(self, request, view, reply):
      if not request.user.is_authenticated:
         return False
      if request.method in SAFE_METHODS: return True
      return request.user == reply.comment.user