"""Tests for accounts models."""
from django.test import TestCase
from django.contrib.auth import get_user_model
from accounts.models import SocialAccount

User = get_user_model()


class UserModelTests(TestCase):
    def test_create_user(self):
        user = User.objects.create_user(username='bob', email='bob@test.com', password='pass')
        self.assertEqual(user.plan, 'free')
        self.assertEqual(user.stripe_customer_id, '')
        self.assertEqual(str(user), 'bob@test.com')

    def test_user_str_fallback_to_username(self):
        user = User.objects.create_user(username='noemail', password='pass')
        self.assertEqual(str(user), 'noemail')


class SocialAccountModelTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='social', password='test')

    def test_create_social_account(self):
        acc = SocialAccount.objects.create(
            user=self.user, provider='twitter', provider_user_id='12345',
            access_token='tok123'
        )
        self.assertIn('Twitter', str(acc))
        self.assertEqual(acc.provider, 'twitter')

    def test_unique_user_provider(self):
        SocialAccount.objects.create(
            user=self.user, provider='twitter', provider_user_id='123',
            access_token='tok'
        )
        with self.assertRaises(Exception):
            SocialAccount.objects.create(
                user=self.user, provider='twitter', provider_user_id='456',
                access_token='tok2'
            )
