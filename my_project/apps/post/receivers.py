from django.db.models.signals import pre_save, post_save, pre_delete, post_delete
from django.dispatch import receiver
from .models import PostModel, PostLikes, PostComments
from django.utils import timezone
import logging


logger = logging.getLogger(__name__)


# pre save method
@receiver(pre_save, sender=PostModel)
def pre_save_post(sender, instance, **kwargs):
	pass


# post save method
@receiver(post_save, sender=PostModel)
def post_save_post(sender, instance, created, **kwargs):
	if created:
		logger.info(f"Post with title: {instance.post_title} successfully created by {instance.post_user.username} at '{timezone.now()}'")
	else:
		logger.info(f"Post with title: {instance.post_title} by {instance.post_user.username} successfully updated at '{timezone.now()}'")


# pre delete method
@receiver(pre_delete, sender=PostModel)
def pre_delete_post(sender, instance, **kwargs):
	pass


# post delete method
@receiver(post_delete, sender=PostModel)
def post_delete_post(sender, instance, **kwargs):
	logger.warning(f"Post with title: {instance.post_title} successfully deleted by {instance.post_user.username} at '{timezone.now()}'")




# pre save likes
@receiver(pre_save, sender=PostLikes)
def pre_save_likes(sender, instance, **kwargs):
	plike = PostLikes.objects.filter(post_id=instance.post_id).filter(liked_by_id=instance.liked_by_id)
	if not plike:
		logger.info(f"User: {instance.liked_by.username} liked post with title: {instance.post_id.post_title} at '{timezone.now()}'")
	else:
		logger.info(f"User: {instance.liked_by.username} disliked post with title: {instance.post_id.post_title} at '{timezone.now()}'")

# post save likes
@receiver(post_save, sender=PostLikes)
def post_save_likes(sender, instance, created, **kwargs):
	pass



# pre delete likes
@receiver(pre_delete, sender=PostLikes)
def pre_delete_likes(sender, instance, **kwargs):
	pass


# post delete likes
@receiver(post_delete, sender=PostLikes)
def post_delete_likes(sender, instance, **kwargs):
	logger.warning(f"User: {instance.liked_by.username} disliked post with title: {instance.post_id.post_title} at '{timezone.now()}'")



# pre save comments
@receiver(pre_save, sender=PostComments)
def pre_save_comments(sender, instance, **kwargs):
	# filtered_com = filter_comments(instance.comment_desc)
	# instance.comment_desc = filtered_com
	if filter_comments(instance.comment_desc):
		raise ValueError("Inappropriate Comment")


# post save comments
@receiver(post_save, sender=PostComments)
def post_save_comments(sender, instance, created, **kwargs):
	if created:
		logger.info(f"User: {instance.com_user.username} commented on post with title: {instance.post.post_title} at '{timezone.now()}'")
	else:
		logger.info(f"User: {instance.com_user.username} changed his comment on post with title: {instance.post.post_title} at '{timezone.now()}'")



# pre delete comments
@receiver(pre_delete, sender=PostComments)	
def pre_delete_comments(sender, instance, **kwargs):
	pass


# post delete comments
@receiver(post_delete, sender=PostComments)
def post_delete_comments(sender, instance, **kwargs):
	logger.warning(f"User: {instance.com_user.username} deleted comment on post with title: {instance.post.post_title} at '{timezone.now()}'")




# function to filter comments
def filter_comments(com):
	restricted = ['terrorism', 'attack', 'kill', 'kidnap', 'shoot', 'bomb', 'gun', 'weapon', 'hatespeech']
	for r in restricted:
		if r in com.lower():
			return True
	return False

	# 		com = com.replace(r, '#@!.&')
	# 		com = com.replace(r.upper(), '#@!.&')

	# return com