from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Profile(models.Model):
   user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
   image = models.ImageField(upload_to='profiles', null=True, blank=True)
   dob = models.DateField(null=True)
   about = models.TextField(null=True)
   sex = models.CharField(max_length=50, choices=[('MALE', 'MALE'), ('FEMALE', 'FEMALE')])
   address = models.CharField(null=True, max_length=500)

class FriendRequest(models.Model):
   sender = models.ForeignKey('auth.User', on_delete=models.CASCADE, related_name="sent_requests")
   receiver = models.ForeignKey('auth.User', on_delete=models.CASCADE, related_name="friend_requests")
   timestamp = models.DateTimeField(auto_now_add=True)

   def __str__(self):
      return "%s wants to be a friend of %s " % (self.sender, self.receiver)

   class Meta:
      unique_together = ['sender', 'receiver']
      ordering = ['-timestamp']


class FriendShip(models.Model):
   friend = models.ForeignKey('auth.User', on_delete=models.CASCADE, related_name="parteners")
   partener = models.ForeignKey('auth.User', on_delete=models.CASCADE, related_name="friends")
   timestamp = models.DateTimeField(auto_now_add=True)

   def __str__(self):
      return "%s is a friend of %s " % (self.friend, self.partener)
   
   class Meta:
      unique_together = ['friend', 'partener']
      ordering = ['-timestamp']

   