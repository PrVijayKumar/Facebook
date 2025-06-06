from django.db import models
# from django.db.models import Lookup, Field
from user.models import CustomUser
# from user.models import User
from django.utils import timezone
import datetime
from django.conf import settings
import os

def get_file_name(instance, filename):
    if instance.id is None:
        old_path = instance.post_content.path
    else:
        old_path = PostModel.objects.get(id=instance.id).post_content.path
    filename = instance.post_content.name
    ar = filename.split('.')
    ext = ar.pop()
    new_name = ""
    for e in ar:
        new_name += e + '.' if e != ar[-1] else e
    instance.post_content.name = f"{new_name}_{instance.id}.{ext}"
    if os.path.exists(old_path):
        new_path = settings.MEDIA_ROOT + '/' + instance.post_content.name	# cannot set path property of ImageFieldFile
        os.rename(old_path, new_path)	# moving the file to a new path)
    return f"images/{instance.post_content.name}"
    # ar = filename.split('.')
    # ext = ar.pop()
    # new_name = ""
    # for e in ar:
    #     new_name += e + '.' if e != ar[-1] else e
    # new_name = f"{new_name}_{instance.id}.{ext}"
    # return "images/" + new_name
    # breakpoint()
    # instance.post_content.path = settings.MEDIA_ROOT + '/' + instance.post_content.name	# cannot set path property of ImageFieldFile
        # breakpoint()
    # instance.save()

# Create your models here.
class PostModel(models.Model):
    post_title = models.CharField(max_length=200)
    # post_user = models.ForeignKey(User, on_delete=models.CASCADE, default=None, related_name="postname")
    post_user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, default=None, related_name="postname")
    # post_user = models.ForeignKey(User, on_delete=models.CASCADE, default=None, related_name="postname")
    post_description = models.TextField()
    # post_content = models.ImageField(upload_to=get_file_name)
    post_content = models.ImageField(upload_to=get_file_name)
    post_date = models.DateTimeField(auto_now_add=True)
    post_updated_date = models.DateTimeField(default=timezone.now)
    # post_likes = models.ManyToManyField(CustomUser, through='PostLikes', related_name="liked_posts")
    post_likes = models.ManyToManyField(CustomUser, related_name='liked_posts', blank=True)
    # post_likes = models.ManyToManyField(default=0)
    post_stars = models.PositiveIntegerField(default=0)
    # post_likes = models.ManyToMany

    def __str__(self):
        return self.post_title
    

    @property
    def like_count(self):
        return self.post_likes.count()
    



# class PostLikes(models.Model):
#     post_id = models.ForeignKey(PostModel, on_delete=models.CASCADE)
#     liked_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='cusers')
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(default=timezone.now)
    # liked_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='users')

    # def __str__(self):
    #     return str(self.post_id)
# class NotEqual(Lookup):
#     lookup_name = "ne"

#     def as_sql(self, compiler, connection):
#         lhs, lhs_params = self.process_lhs(compiler, connection)
#         rhs, rhs_params = self.process_rhs(compiler, connection)
#         params = lhs_params + rhs_params
#         return "%s <> %s" % (lhs, rhs), params


# Field.register_lookup(NotEqual)


class PostComments(models.Model):
    comment_desc = models.CharField(max_length=200, null=False)
    post = models.ForeignKey(PostModel, on_delete=models.CASCADE, related_name="pcom")
    com_user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="commenters")
    # com_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="commenters")
    com_date = models.DateTimeField(auto_now_add=True)
    com_reply = models.ForeignKey(CustomUser, on_delete=models.CASCADE, default=None, related_name="repliers", null=True)
    # com_reply = models.ForeignKey(User, on_delete=models.CASCADE, default=None, related_name="repliers", null=True)
    com_likes = models.PositiveIntegerField(default=0)
    # reply_on_comment = models.PositiveIntegerField(null=True)
    reply_on_comment = models.ForeignKey('self', on_delete=models.CASCADE, related_name='replies', null=True, blank=True)
    # created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

class PostStars(models.Model):
    post = models.ForeignKey(PostModel, on_delete=models.CASCADE)
    nos = models.PositiveIntegerField(default=0)
    sent_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)




# class Price(models.Model):
#     product = models.ForeignKey(Stars, on_delete=models.CASCADE)
#     stripe_price_id = models.CharField(max_length=100)
#     price = models.IntegerField(default=0)  # cents


#     def __str__(self):
#         return "{0:.2f}".format(self.price / 100)