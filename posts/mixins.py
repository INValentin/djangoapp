from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from .serializers import LikeSerializer

# class PaginatedAction:
#    def action_pagination(queryset, serializer, request=None):
      


class LikeAction:
   @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated,])
   def like(self, request, pk=None):
      obj = self.get_object()
      if request.user in obj.likes.all():
         obj.likes.remove(request.user)
      else: obj.likes.add(request.user)
      return Response(LikeSerializer(obj).data, status=200)

class ChildList:
   def list_child(self, request, pk=None):
      obj = self.get_object()
      queryset = self.get_child_queryset(obj)
      page = self.paginate_queryset(queryset)
      serializer = self.child_serializer(page, many=True, context={'request': request})
      return self.get_paginated_response(serializer.data)