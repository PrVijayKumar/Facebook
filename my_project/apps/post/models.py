from django.db import models
# from django.db.models import Lookup, Field
from user.models import CustomUser
# from user.models import User
from django.utils import timezone
import datetime

# Create your models here.
class PostModel(models.Model):
    post_title = models.CharField(max_length=200)
    # post_user = models.ForeignKey(User, on_delete=models.CASCADE, default=None, related_name="postname")
    post_user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, default=None, related_name="postname")
    # post_user = models.ForeignKey(User, on_delete=models.CASCADE, default=None, related_name="postname")
    post_description = models.TextField()
    post_content = models.ImageField(upload_to='images/')
    post_date = models.DateTimeField(auto_now_add=True)
    post_updated_date = models.DateTimeField(default=timezone.now)
    post_likes = models.PositiveIntegerField(default=0)
    post_stars = models.PositiveIntegerField(default=0)
    # post_likes = models.ManyToMany

    def __str__(self):
        return self.post_title


class PostLikes(models.Model):
    post_id = models.ForeignKey(PostModel, on_delete=models.CASCADE)
    liked_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='cusers')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(default=timezone.now)
    # liked_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='users')

    def __str__(self):
        return str(self.post_id)
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
    reply_on_comment = models.PositiveIntegerField(null=True)
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