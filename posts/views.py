from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from .models import Post
from .publish import publish_due_posts_for_user
from allauth.socialaccount.models import SocialAccount as AllAuthSocialAccount
from datetime import datetime
import traceback

SUPPORTED_PLATFORMS = ['twitter', 'linkedin']
OAUTH_PROVIDER_MAP = {
    'twitter': 'twitter_oauth2',
    'linkedin': 'linkedin_oauth2',
}
OAUTH_PROVIDER_REVERSE = {v: k for k, v in OAUTH_PROVIDER_MAP.items()}
PLATFORM_LABELS = {
    'twitter': 'Twitter/X',
    'linkedin': 'LinkedIn',
    'instagram': 'Instagram',
}


def get_connected_platforms(user):
    manual = set(user.social_accounts.values_list('provider', flat=True))
    oauth_providers = set(AllAuthSocialAccount.objects.filter(user=user).values_list('provider', flat=True))
    oauth = {OAUTH_PROVIDER_REVERSE.get(provider, provider) for provider in oauth_providers}
    return manual | oauth


def platform_validation(request, platforms):
    if not platforms:
        messages.error(request, 'Select at least one platform to publish to.')
        return False

    unsupported = [p for p in platforms if p not in SUPPORTED_PLATFORMS]
    if unsupported:
        messages.error(request, 'The following platforms are not supported yet: ' +
            ', '.join(PLATFORM_LABELS.get(p, p) for p in unsupported) + '.')
        return False

    connected = get_connected_platforms(request.user)
    missing = [p for p in platforms if p not in connected]
    if missing:
        messages.error(request, 'Connect ' + ', '.join(PLATFORM_LABELS[p] for p in missing) + ' before publishing there.')
        return False

    return True

def home(request):
    return render(request, 'pages/home.html')

def pricing(request):
    return render(request, 'pages/pricing.html')

@login_required
def dashboard(request):
    posts = Post.objects.filter(user=request.user)[:20]
    scheduled = Post.objects.filter(user=request.user, status='scheduled').count()
    published = Post.objects.filter(user=request.user, status='published').count()
    connected = get_connected_platforms(request.user)
    return render(request, 'dashboard/index.html', {
        'posts': posts,
        'scheduled': scheduled,
        'published': published,
        'connected_platforms': connected,
    })

@login_required
def create_post(request):
    if request.method == 'POST':
        content = request.POST.get('content', '').strip()
        schedule = request.POST.get('scheduled_at', '').strip()
        platforms = request.POST.getlist('platforms')

        if not content:
            messages.error(request, "Post content is required.")
            return redirect('posts:create_post')

        if not platform_validation(request, platforms):
            return redirect('posts:create_post')

        scheduled_at = None
        if schedule:
            scheduled_at = datetime.fromisoformat(schedule)
            if timezone.is_naive(scheduled_at):
                scheduled_at = timezone.make_aware(scheduled_at, timezone.get_current_timezone())

        post = Post(
            user=request.user,
            content=content,
            platforms=platforms,
            status='scheduled' if scheduled_at else 'draft',
            scheduled_at=scheduled_at,
        )
        post.content_variants = {
            'twitter': content[:280] if len(content) > 280 else content,
            'linkedin': content,
        }
        post.save()
        messages.success(request, "Post created successfully.")
        return redirect('posts:dashboard')

    return render(request, 'posts/create.html', {
        'now': timezone.now().strftime('%Y-%m-%dT%H:%M'),
        'connected_platforms': get_connected_platforms(request.user),
        'supported_platforms': SUPPORTED_PLATFORMS,
        'platform_labels': PLATFORM_LABELS,
    })

@login_required
def edit_post(request, pk):
    post = get_object_or_404(Post, pk=pk, user=request.user)
    if request.method == 'POST':
        content = request.POST.get('content', '').strip()
        schedule = request.POST.get('scheduled_at', '').strip()
        platforms = request.POST.getlist('platforms')
        if not content:
            messages.error(request, "Post content is required.")
            return redirect('posts:edit_post', pk=pk)
        if not platforms:
            platforms = post.platforms

        if not platform_validation(request, platforms):
            return redirect('posts:edit_post', pk=pk)

        post.content = content
        post.platforms = platforms
        if schedule:
            scheduled_at = datetime.fromisoformat(schedule)
            if timezone.is_naive(scheduled_at):
                scheduled_at = timezone.make_aware(scheduled_at, timezone.get_current_timezone())
            post.scheduled_at = scheduled_at
            post.status = 'scheduled'
        elif not post.scheduled_at:
            post.status = 'draft'
        post.content_variants = {
            'twitter': content[:280] if len(content) > 280 else content,
            'linkedin': content,
        }
        post.save()
        messages.success(request, "Post updated successfully.")
        return redirect('posts:dashboard')
    return render(request, 'posts/edit.html', {
        'post': post,
        'now': timezone.now().strftime('%Y-%m-%dT%H:%M'),
        'connected_platforms': get_connected_platforms(request.user),
        'supported_platforms': SUPPORTED_PLATFORMS,
        'platform_labels': PLATFORM_LABELS,
    })

@login_required
def delete_post(request, pk):
    post = get_object_or_404(Post, pk=pk, user=request.user)
    post.delete()
    messages.success(request, "Post deleted.")
    return redirect('posts:dashboard')

@login_required
def publish_due_posts(request):
    results = publish_due_posts_for_user(request.user)
    if not results:
        messages.info(request, 'No due posts were ready to publish.')
    else:
        for post, success, message in results:
            if success:
                messages.success(request, f'Published post {post.pk}.')
            else:
                messages.error(request, f'Post {post.pk} failed: {message}')

    return redirect('posts:dashboard')
