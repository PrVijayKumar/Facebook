from django.urls import path
from . import views
from django.views.decorators.cache import cache_page
app_name = "post"

urlpatterns = [
    path('createpost/', views.create_post, name='cpost'),
    path('myposts/', views.my_posts, name='mpost'),
    # path('allposts/', views.all_posts, name="apost"),
    path('fposts/', views.friend_posts, name="fpost"),
    path('myposts/edit/<int:id>', views.edit_posts, name="epost"),
    path('myposts/dpost/<int:id>', views.del_post, name="dpost"),
    path('myposts/detpost/<int:id>', cache_page(10*60)(views.det_post), name="detpost"),
    path('lpost/<int:id>', views.like_post, name="lpost"),
    path('comments/<int:id>', views.comment_post, name="comment"),
    path('fcomments/<int:id>', views.fetch_comments, name="fcomments"),
    path('freplies/<int:id>', views.fetch_replies, name="fr"),
    path('cedit/<int:id>', views.edit_comment, name="ec"),
    path('cdelete/<int:id>', views.delete_comment, name="dc"),
    # path('checkout/<int:post_id>', views.CheckoutView.as_view(), name="checkout"),
    path('create-payment/<int:post_id>', views.CreatePaymentView.as_view(), name="create_payment"),
    # path('success/', views.success, name="success"),
    # path('cancel', views.cancel, name="cancel"),
]
