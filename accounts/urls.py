from django.urls import path
from rest_framework.routers import DefaultRouter

from rest_framework_simplejwt.views import token_obtain_pair, token_refresh

from .views import (
   CurrentUserView,
   RegisterUserView,
   UserViewSet,
   ReadNotification,
   ReadAllNotifications,
   RetrieveDeleteNotification,
   FriendRequestViewSet,
   FriendShipViewSet,
)

router = DefaultRouter()

router.register(r'users', UserViewSet)
router.register(r'friend_requests', FriendRequestViewSet)
router.register(r'friend_ships', FriendShipViewSet)

urlpatterns = [
   path('notifications/<int:pk>/', RetrieveDeleteNotification.as_view(), name="retrieve-delete-notification"),
   path('users/read-notification/<int:pk>/', ReadNotification.as_view(), name='read-notification'),
   path('users/read-all-notifications/', ReadAllNotifications.as_view(), name='read-all-notifications'),
   path('auth/register/', RegisterUserView.as_view(), name="register"),
   path('auth/current/', CurrentUserView.as_view(), name="currentuser"),
   path('auth/token/', token_obtain_pair, name="token_obtain"),
   path('auth/token/refresh/', token_refresh, name="token_refresh"),
]

urlpatterns += router.urls

