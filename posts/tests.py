"""Tests for posts models."""
from django.test import TestCase
from django.contrib.auth import get_user_model
from posts.models import Post

User = get_user_model()


class PostModelTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='tester', password='test')

    def test_create_post_defaults(self):
        post = Post.objects.create(user=self.user, content='Hello')
        self.assertEqual(post.status, 'draft')
        self.assertEqual(post.platforms, [])
        self.assertEqual(post.content_variants, {})
        self.assertEqual(post.error, '')
        self.assertEqual(post.platform_count, 0)

    def test_post_with_platforms(self):
        post = Post.objects.create(
            user=self.user, content='Multi-post',
            platforms=['twitter', 'linkedin']
        )
        self.assertEqual(post.platform_count, 2)

    def test_post_str(self):
        post = Post.objects.create(user=self.user, content='Hello world!', status='published')
        self.assertIn('Hello world!', str(post))
        self.assertIn('published', str(post))

    def test_post_ordering(self):
        from datetime import timedelta
        from django.utils import timezone
        p1 = Post.objects.create(user=self.user, content='A',
            scheduled_at=timezone.now() + timedelta(hours=2))
        p2 = Post.objects.create(user=self.user, content='B',
            scheduled_at=timezone.now() + timedelta(hours=1))
        p3 = Post.objects.create(user=self.user, content='C')  # no scheduled_at
        posts = list(Post.objects.all())
        # p1 scheduled later, should come first (descending order)
        self.assertEqual(posts[0], p1)
