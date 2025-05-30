from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse
from .models import PostModel, Stars, PostLikes

User = get_user_model()

class MyPostsViewTest(TestCase):
    def setUp(self):
        # Create a test user
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client = Client()
        self.client.login(username='testuser', password='testpassword')

        # Create test stars for the user
        self.stars = Stars.objects.create(user=self.user, amount=5)

        # Create test posts for the user
        for i in range(10):
            PostModel.objects.create(
                post_title=f"Test Post {i}",
                post_description=f"Description {i}",
                post_content=f"Content {i}",
                post_user=self.user
            )

        # Create liked posts
        self.liked_post = PostModel.objects.first()
        PostLikes.objects.create(post_id=self.liked_post, liked_by=self.user)

    def test_my_posts_view(self):
        # Send a GET request to the my_posts view
        response = self.client.get(reverse('my_posts'))

        # Check if the response is successful
        self.assertEqual(response.status_code, 200)

        # Check if the correct template is used
        self.assertTemplateUsed(response, 'post/myposts.html')

        # Check if the posts are paginated
        self.assertIn('posts', response.context)
        self.assertEqual(len(response.context['posts']), 5)  # 5 posts per page

        # Check if the liked posts are included in the context
        self.assertIn('likes', response.context)
        self.assertIn(self.liked_post.id, response.context['likes'])

        # Check if the number of stars is correct
        self.assertEqual(response.context['nos'], 5)

    def test_pagination(self):
        # Test the second page of posts
        response = self.client.get(reverse('my_posts') + '?page=2')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['posts']), 5)  # Remaining 5 posts