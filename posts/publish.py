from django.utils import timezone
from allauth.socialaccount.models import SocialToken
from accounts.models import SocialAccount as CustomSocialAccount
from accounts.social_clients import SocialPublishError, publish_post_to_provider
from .models import Post

OAUTH_PROVIDER_MAP = {
    'twitter': 'twitter_oauth2',
    'linkedin': 'linkedin_oauth2',
}


def get_publish_account(user, provider):
    oauth_provider = OAUTH_PROVIDER_MAP.get(provider, provider)
    token = SocialToken.objects.filter(account__user=user, account__provider=oauth_provider).first()
    if token:
        return token
    return CustomSocialAccount.objects.filter(user=user, provider=provider).first()


def publish_due_posts_for_user(user=None):
    now = timezone.now()
    posts = Post.objects.filter(status='scheduled', scheduled_at__lte=now).order_by('scheduled_at')
    if user is not None:
        posts = posts.filter(user=user)
    results = []

    for post in posts:
        try:
            platforms = post.platforms or []
            if not platforms:
                raise SocialPublishError('No platforms configured for this post.')

            for provider in platforms:
                account = get_publish_account(post.user, provider)
                if not account:
                    raise SocialPublishError(f'No connected account for {provider}.')
                publish_post_to_provider(post, account)

            post.status = 'published'
            post.published_at = timezone.now()
            post.error = ''
            post.save()
            results.append((post, True, 'Published successfully.'))
        except SocialPublishError as exc:
            post.status = 'failed'
            post.error = str(exc)
            post.save()
            results.append((post, False, str(exc)))

    return results
