from django.dispatch import receiver
from django.contrib.auth.models import User
from django.db.models.signals import m2m_changed, post_save

from posts.models import Post, Comment, Reply, BaseNotification

def like(action, model, on_obj_owner, on_obj_id, on_model_name, instance, pk_set, _type, model_name):
   if (not action == 'post_add'):
      return
   
   liked_user = model.objects.get(pk=list(pk_set)[0])
   
   notification = BaseNotification.objects.create(
      user=liked_user,
      _type=_type,
      model=model_name,
      obj_id=instance.id,
      on_model=on_model_name,
      on_obj_id=on_obj_id,
      on_obj_owner=on_obj_owner,
   )

   for user in instance.likes.all():
      if user != liked_user:
         notification.recievers.add(user)
   
   if instance.user != liked_user:
      notification.recievers.add(instance.user)
   else:
      notification.recievers.remove(instance.user)


@receiver(signal=post_save, sender=Post, dispatch_uid="post_create")
def post_created(sender, instance, raw, created, **kwargs):
   if not created:
      return print("Instance not created")
   
   notification = BaseNotification.objects.create(user=instance.user, _type='post_create', model='Post', obj_id=instance.id)
   
   for user in User.objects.all():
      if user != instance.user:
         notification.recievers.add(user)

# create a comment notification on new comment

@receiver(signal=post_save, sender=Comment, dispatch_uid="comment_create")
def comment_created(sender, instance, raw, created, **kwargs):
   if not created:
      return print("Instance not created")

   notification = BaseNotification.objects.create(user=instance.user, _type="comment_create", model="Comment", on_obj_owner= instance.post.user, obj_id=instance.id, on_model='Post', on_obj_id=instance.post.id)
   
   for comment in instance.post.comments.all():
      if comment.user != instance.user:
         notification.recievers.add(comment.user)
   
   if instance.post.user != instance.user:
      notification.recievers.add(instance.post.user)
   else:
      notification.recievers.remove(instance.post.user)

# reply create notification

@receiver(signal=post_save, sender=Reply, dispatch_uid="reply_create")
def reply_created(sender, instance, raw, created, **kwargs):
   if not created:
      return print("Instance not created")

   notification = BaseNotification.objects.create(user=instance.user, _type="reply_create", model="Reply", on_obj_owner= instance.comment.user, obj_id=instance.id, on_model='Comment', on_obj_id=instance.comment.id)

   for reply in instance.comment.replies.all():
      if reply.user != instance.user:
         notification.recievers.add(reply.user)  
   
   if instance.comment.user != instance.user:
      notification.recievers.add(instance.comment.user)
   else:
      notification.recievers.remove(instance.comment.user)

# post like notification

@receiver(signal=m2m_changed, sender=Post.likes.through, dispatch_uid="post_like")
def post_liked(action, instance, reverse, model, pk_set, **kwargs):
   like(action=action, on_obj_owner= None, on_model_name=None, on_obj_id=None, model=model, instance=instance, pk_set=pk_set, _type='like_post', model_name='Post')


# comment like notification

@receiver(signal=m2m_changed, sender=Comment.likes.through, dispatch_uid="comment_like")
def comment_liked(action, instance, reverse, model, pk_set, **kwargs):
   like(action=action, on_obj_owner= instance.post.user, on_model_name='Post', on_obj_id=instance.post.id, model=model, instance=instance, pk_set=pk_set, _type='like_comment', model_name='Comment')


# reply like notification

@receiver(signal=m2m_changed, sender=Reply.likes.through, dispatch_uid="reply_like")
def reply_liked(action, instance, reverse, model, pk_set, **kwargs):
   like(action=action, on_obj_owner= instance.comment.user, on_model_name='Comment', on_obj_id=instance.comment.id, model=model, instance=instance, pk_set=pk_set, _type='like_reply', model_name='Reply')

