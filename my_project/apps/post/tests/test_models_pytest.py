import pytest
from django.utils import timezone


def test_create_post(new_post):
    user1, post = new_post
    assert post.post_title == "Test Post"
    assert post.post_user == user1
    assert post.post_description == "This post is created for testing purpose."
    assert post.post_content == "images/yellowcar.webp"
    assert str(post.post_date.date()) == str(timezone.now().date())
    assert str(post.post_updated_date.date()) == str(timezone.now().date())
    assert post.post_likes == 0
    assert str(post) == post.post_title


def test_post_comment(postcom):
    comment, reply, user1, post = postcom
    assert comment.comment_desc == "Test Comment"
    assert comment.post == post
    assert comment.com_user == user1
    assert str(comment.com_date.date()) == str(timezone.now().date())
    assert comment.com_reply is None
    assert comment.com_likes == 0
    assert comment.reply_on_comment is None
    assert str(comment.updated_at.date()) == str(timezone.now().date())
    assert reply.comment_desc == "Test Reply"
    assert reply.post == post
    assert reply.com_user == user1
    assert reply.com_reply == user1
    assert reply.reply_on_comment == comment.id
    assert str(reply.com_date.date()) == str(timezone.now().date())
    assert reply.com_likes == 0
    assert reply.reply_on_comment == comment.id
    assert str(reply.updated_at.date()) == str(timezone.now().date())


def test_post_likes(postlike):
    user, post, like = postlike
    assert like.post_id == post
    assert like.liked_by == user
    assert str(like.created_at.date()) == str(timezone.now().date())
    assert str(like.updated_at.date()) == str(timezone.now().date())
    assert str(like) == str(like.post_id)



def test_new_post(post_model_factory):
    post = post_model_factory.build()
    print(post.post_title)
    assert True

def test_new_comment(post_comments_factory):
    comment = post_comments_factory.build()
    print(comment.comment_desc)
    assert True

def test_new_likes(post_likes_factory):
    like = post_likes_factory.build()
    print(like.liked_by)
    assert True


def test_new_cpost(new_cpost):
    post = new_cpost
    print(post.post_title)
    assert True

def test_new_ccomment(new_ccomment):
    comment = new_ccomment
    print(comment.comment_desc)
    assert True

def test_new_clike(new_clike):
    like = new_clike
    print(like.liked_by)
    assert True