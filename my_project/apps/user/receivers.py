from django.db.models.signals import pre_save, post_save, pre_delete, post_delete
from django.contrib.auth.signals import user_logged_in, user_logged_out, user_login_failed
from django.dispatch import receiver, Signal
from .models import CustomUser
from post.models import PostModel
import logging
from django.utils import timezone
from . import signals
from django.conf import settings
from ipware import get_client_ip
from django.core.cache import cache
logger = logging.getLogger(__name__)




# User Login Signal
@receiver(user_logged_in, sender=CustomUser)
def login_success(sender, request, user, **kwargs):
	signals.request_by_user.send(sender=CustomUser, username=user.username, request=request)
	logger.info(f"User with username: '{user.username}' successfully logged in at '{timezone.now()}'")

# user_logged_in.connect(login_success, sender=CustomUser)


# User Logout Signal
@receiver(user_logged_out, sender=CustomUser)
def log_out(sender, request, user, **kwargs):
	cache.clear()
	logger.info(f"User with username: '{user.username}' successfully logged out at '{timezone.now()}'")

# user_logged_out.connect(log_out, sender=CustomUser)



# User Login Failed
@receiver(user_login_failed)
def login_failed(sender, credentials, request, **kwargs):
	if request is not None:
		signals.request_by_user.send(sender=CustomUser, username=credentials['username'],request=request)
	print('reached')
	logger.warning(f"Anonymous user with credentials: '{credentials}' was restricted from logging in at '{timezone.now()}'")

# user_login_failed.connect(login_failed)

# Pre-save Signal
@receiver(pre_save, sender=CustomUser)
def pre_save_user(sender, instance, **kwargs):
	instance.updated_at = timezone.now()


# Post-save Signal
@receiver(post_save, sender=CustomUser)
def post_save_user(sender, instance, created, **kwargs):
	if created:
		logger.info(f"New User Created with username:'{instance.username}' at '{timezone.now()}'")
	else:
		logger.info(f"User Profile with username:'{instance.username}' successfully updated at '{timezone.now()}'")


# Pre-delete Signal
@receiver(pre_delete, sender=CustomUser)
def pre_delete_user(sender, instance, **kwargs):
	pass

# Post-delete Signal
@receiver(post_delete, sender=CustomUser)
def post_delete_user(sender, instance, **kwargs):
	logger.warning(f"User with username: '{instance.username}' was successfully deleted at '{timezone.now()}'")




# Custom Signal
@receiver(signals.request_by_user, sender=CustomUser)
def log_ip(sender, username, request, **kwargs):
	# request.META['REMOTE_ADDR'] = '127.0.0.1'
	client_ip, is_routable = get_client_ip(request)
	if client_ip is None:
		logger.info(f"Unable to get the ip address of User: {username}")
	else:
		if is_routable:
			logger.info(f"User with username: '{username}' attempted to log in with \n\t IP Address: {client_ip} \n\t at '{timezone.now()}'")
		else:
			logger.info(f"The IP address of User : {username} is private.")



# creating dummpy post when first login

@receiver(signals.create_dummy_post, sender=CustomUser)
def sd_post(sender, user, **kwargs):
	if user.last_login is None:
		post = PostModel.objects.create(
				post_title="Dummy Post",
				post_description="This is a Dummy Post",
				post_content="images/yellowcar.webp",
				post_user=user
			)
		# post.save()