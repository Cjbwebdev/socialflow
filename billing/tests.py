"""Tests for billing models."""
from django.test import TestCase
from django.contrib.auth import get_user_model
from billing.models import Subscription

User = get_user_model()


class SubscriptionModelTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='subber', password='test')

    def test_create_subscription_defaults(self):
        sub = Subscription.objects.create(user=self.user)
        self.assertEqual(sub.plan, 'free')
        self.assertTrue(sub.active)
        self.assertEqual(sub.stripe_subscription_id, '')

    def test_subscription_str(self):
        self.user.email = 'sub@example.com'
        self.user.save()
        sub = Subscription.objects.create(user=self.user, plan='pro')
        self.assertIn('sub@example.com', str(sub))
        self.assertIn('pro', str(sub))

    def test_one_to_one_user(self):
        Subscription.objects.create(user=self.user)
        with self.assertRaises(Exception):
            Subscription.objects.create(user=self.user)
