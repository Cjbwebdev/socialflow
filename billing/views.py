import os
import stripe
from django.conf import settings
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, JsonResponse
from django.views.decorators.http import require_POST
from .models import Subscription

if settings.STRIPE_SECRET_KEY:
    stripe.api_key = settings.STRIPE_SECRET_KEY

SITE_URL = os.getenv('SITE_URL', 'http://localhost:8000')

PRICE_MAP = {
    'pro': settings.STRIPE_PRICE_ID_PRO,
}


@login_required
@require_POST
def create_checkout_session(request):
    plan = request.POST.get('plan', 'pro')
    price_id = PRICE_MAP.get(plan)
    if not price_id:
        return JsonResponse({'error': f'Invalid plan: {plan}'}, status=400)
    
    try:
        session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            mode='subscription',
            line_items=[{
                'price': price_id,
                'quantity': 1,
            }],
            success_url=f'{SITE_URL}/billing/success/?session_id=' + '{CHECKOUT_SESSION_ID}',
            cancel_url=f'{SITE_URL}/pricing/',
            customer_email=request.user.email,
            metadata={'user_id': str(request.user.id), 'plan': plan},
        )
        return redirect(session.url)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@login_required
def checkout_success(request):
    session_id = request.GET.get('session_id')
    if session_id:
        try:
            session = stripe.checkout.Session.retrieve(session_id)
            if session.payment_status == 'paid':
                user_id = session.metadata.get('user_id')
                plan = session.metadata.get('plan', 'pro')
                if user_id and int(user_id) == request.user.id:
                    sub, _ = Subscription.objects.get_or_create(user=request.user)
                    sub.plan = plan
                    sub.stripe_subscription_id = session.get('subscription', '')
                    sub.active = True
                    sub.save()
        except Exception:
            pass
    return render(request, 'billing/success.html')


@csrf_exempt
def webhook(request):
    payload = request.body
    sig = request.META.get('HTTP_STRIPE_SIGNATURE', '')
    
    try:
        event = stripe.Webhook.construct_event(
            payload, sig, settings.STRIPE_WEBHOOK_SECRET
        )
    except (ValueError, stripe.error.SignatureVerificationError):
        return HttpResponse(status=400)
    
    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']
        user_id = session.get('metadata', {}).get('user_id')
        plan = session.get('metadata', {}).get('plan', 'pro')
        if user_id:
            from django.contrib.auth import get_user_model
            User = get_user_model()
            try:
                user = User.objects.get(id=user_id)
                sub, _ = Subscription.objects.get_or_create(user=user)
                sub.plan = plan
                sub.stripe_subscription_id = session.get('subscription', '')
                sub.active = True
                sub.save()
            except User.DoesNotExist:
                pass
    
    elif event['type'] == 'customer.subscription.deleted':
        sub_id = event['data']['object']['id']
        try:
            sub = Subscription.objects.get(stripe_subscription_id=sub_id)
            sub.active = False
            sub.plan = 'free'
            sub.save()
        except Subscription.DoesNotExist:
            pass
    
    return HttpResponse(status=200)


@login_required
def subscription_status(request):
    sub = getattr(request.user, 'subscription', None)
    return render(request, 'billing/status.html', {'subscription': sub})


def pricing(request):
    return render(request, 'pages/pricing.html')
