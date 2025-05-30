import pytest
from post.models import PostModel, PostComments, PostLikes


# def test_post(db, post_model_factory):
#     post = post_model_factory.create()
#     print(post.post_description)
#     assert True

# def test_comment(db, post_comments_factory):
#     comment = post_comments_factory.create()
#     print(comment.comment_desc)
#     assert True

# using parametrizing to test model
@pytest.mark.parametrize(
    "post_title, post_user, post_description, post_content, validity",
    [
        ("Test Post", 1, "This post is created for testing purpose.", "images/yellowcar.webp", True),
        ("Test", 1, "This post is created for testing.", "images/yellowcar.webp", True),
    ]
)
def test_post_instance(
    db, post_model_factory, post_title, post_user, post_description, post_content, validity
):
    test = post_model_factory(
        post_title=post_title,
        post_user_id=post_user,
        post_description=post_description,
        post_content=post_content
    )
    # breakpoint()

    item = PostModel.objects.all().count()
    assert item == validity

# @pytest.mark.parametrize(
#     "comment_desc, post, com_user, com_date, com_reply, com_likes, reply_on_comment, updated_at",
#     [
#         ()
#     ]
# )
# def test_post_instance()