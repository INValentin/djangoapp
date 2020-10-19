from django.db import models

# Create your models here.

class Like(models.Model):
   user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
   timestamp = models.DateTimeField(auto_now_add=True)
   
   class Meta:
      abstract = True

class PostLike(Like):
   post = models.ForeignKey('Post', on_delete=models.CASCADE)
   
   def __str__(self):
      return '(%s) liked (%s) at %s' % (self.user, self.post, self.timestamp)

class CommentLike(Like):
   comment = models.ForeignKey('Comment', on_delete=models.CASCADE)

   def __str__(self):
      return '(%s) liked (%s) at %s' % (self.user, self.comment, self.timestamp)

class ReplyLike(Like):
   reply = models.ForeignKey('Reply', on_delete=models.CASCADE)

   def __str__(self):
      return '(%s) liked (%s) at %s' % (self.user, self.reply, self.timestamp)


class Post(models.Model):
   user = models.ForeignKey('auth.User', on_delete=models.CASCADE, related_name='posts')
   caption = models.CharField(max_length=150)
   content = models.TextField(null=True, blank=True)
   image = models.ImageField(upload_to='posts', null=True, blank=True)
   likes = models.ManyToManyField('auth.User', through=PostLike, blank=True,  default=0)
   created_at = models.DateTimeField(auto_now_add=True)
   updated_at = models.DateTimeField(null=True, blank=True)

   class Meta:
      ordering = ['-created_at']

   def __str__(self):
      return self.content

class Comment(models.Model):
   user = models.ForeignKey('auth.User', on_delete=models.CASCADE, related_name='comments')
   post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
   content = models.TextField()
   likes = models.ManyToManyField('auth.User', blank=True, default=0, through=CommentLike)
   created_at = models.DateTimeField(auto_now_add=True)
   updated_at = models.DateTimeField(null=True, blank=True)

   class Meta:
      ordering = ['-created_at']
   
   def __str__(self):
      return self.content
   
class Reply(models.Model):
   user = models.ForeignKey('auth.User', on_delete=models.CASCADE, related_name='replies')
   comment = models.ForeignKey(Comment, on_delete=models.CASCADE, related_name='replies')
   content = models.TextField()
   likes = models.ManyToManyField('auth.User', blank=True, default=0, through=ReplyLike)
   created_at = models.DateTimeField(auto_now_add=True)
   updated_at = models.DateTimeField(null=True, blank=True)

   class Meta:
      ordering = ['-created_at']

   def __str__(self):
      return self.content
   
# notifications model

class BaseNotification(models.Model):
   user = models.ForeignKey('auth.User', on_delete=models.CASCADE, related_name='actions')
   _type = models.CharField(max_length=50)
   model = models.CharField(max_length=50, null=True)
   obj_id = models.IntegerField(null=True)
   on_model = models.CharField(max_length=50, null=True)
   on_obj_id = models.IntegerField(null=True)
   is_read = models.BooleanField(default=False)
   on_obj_owner = models.ForeignKey('auth.User', on_delete=models.CASCADE, related_name="my_notifications", null=True)
   timestamp = models.DateTimeField(auto_now_add=True)
   recievers = models.ManyToManyField('auth.User', related_name='notifications')
   seen_by = models.ManyToManyField('auth.User', related_name='seen_notifications')

   def __str__(self):
      return "%s did %s" % (self.user, self._type)
   
   class Meta:
      ordering = ['-timestamp',]
