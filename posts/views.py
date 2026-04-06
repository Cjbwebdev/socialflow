from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from .models import Post
from datetime import datetime
import traceback

def home(request):
    return render(request, 'pages/home.html')

def pricing(request):
    return render(request, 'pages/pricing.html')

@login_required
def dashboard(request):
    posts = Post.objects.filter(user=request.user)[:20]
    scheduled = Post.objects.filter(user=request.user, status='scheduled').count()
    published = Post.objects.filter(user=request.user, status='published').count()
    return render(request, 'dashboard/index.html', {
        'posts': posts,
        'scheduled': scheduled,
        'published': published,
    })

@login_required
def create_post(request):
    if request.method == 'POST':
        content = request.POST.get('content', '').strip()
        schedule = request.POST.get('scheduled_at', '').strip()
        platforms = request.POST.getlist('platforms')
        if not content:
            messages.error(request, "Post content is required.")
            return redirect('create_post')
        if not platforms:
            platforms = ['twitter']

        post = Post(
            user=request.user,
            content=content,
            platforms=platforms,
            status='scheduled' if schedule else 'draft',
            scheduled_at=datetime.fromisoformat(schedule) if schedule else None,
        )
        post.content_variants = {
            'twitter': content[:280] if len(content) > 280 else content,
            'linkedin': content,
        }
        post.save()
        messages.success(request, "Post created successfully.")
        return redirect('dashboard')

    return render(request, 'posts/create.html', {
        'now': timezone.now().strftime('%Y-%m-%dT%H:%M')
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
            return redirect('edit_post', pk=pk)
        if not platforms:
            platforms = post.platforms
        post.content = content
        post.platforms = platforms
        if schedule:
            post.scheduled_at = datetime.fromisoformat(schedule)
            post.status = 'scheduled' if post.scheduled_at > timezone.now() else 'scheduled'
        elif not post.scheduled_at:
            post.status = 'draft'
        post.content_variants = {
            'twitter': content[:280] if len(content) > 280 else content,
            'linkedin': content,
        }
        post.save()
        messages.success(request, "Post updated successfully.")
        return redirect('dashboard')
    return render(request, 'posts/edit.html', {
        'post': post,
        'now': timezone.now().strftime('%Y-%m-%dT%H:%M')
    })

@login_required
def delete_post(request, pk):
    post = get_object_or_404(Post, pk=pk, user=request.user)
    post.delete()
    messages.success(request, "Post deleted.")
    return redirect('dashboard')
