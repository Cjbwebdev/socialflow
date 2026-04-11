from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django import forms
from allauth.socialaccount.models import SocialAccount as AllAuthSocialAccount
from .models import User, SocialAccount
from .forms import SocialAccountForm

class RegisterForm(forms.ModelForm):
    password1 = forms.CharField(widget=forms.PasswordInput, label='Password')
    password2 = forms.CharField(widget=forms.PasswordInput, label='Confirm Password')
    
    class Meta:
        model = User
        fields = ['email', 'username']
    
    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return cleaned_data
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
        return user

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            return redirect('posts:dashboard')
    else:
        form = AuthenticationForm()
    return render(request, 'accounts/login.html', {'form': form})

def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('posts:dashboard')
    else:
        form = RegisterForm()
    return render(request, 'accounts/register.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('posts:home')

@login_required
def social_accounts_view(request):
    if request.method == 'POST':
        form = SocialAccountForm(request.POST)
        if form.is_valid():
            provider = form.cleaned_data['provider']
            account, created = SocialAccount.objects.update_or_create(
                user=request.user,
                provider=provider,
                defaults={
                    'provider_user_id': form.cleaned_data['provider_user_id'],
                    'access_token': form.cleaned_data['access_token'],
                    'refresh_token': form.cleaned_data.get('refresh_token', ''),
                    'expires_at': form.cleaned_data.get('expires_at'),
                }
            )
            action = 'Connected' if created else 'Updated'
            messages.success(request, f'{action} {provider.capitalize()} account successfully.')
            return redirect('accounts:social_accounts')
    else:
        form = SocialAccountForm()

    social_accounts = request.user.social_accounts.all()
    allauth_connected = set(AllAuthSocialAccount.objects.filter(user=request.user).values_list('provider', flat=True))
    available_providers = [
        {'id': 'twitter_oauth2', 'label': 'Twitter/X'},
        {'id': 'linkedin_oauth2', 'label': 'LinkedIn'},
    ]
    provider_labels = {
        'twitter_oauth2': 'Twitter/X',
        'linkedin_oauth2': 'LinkedIn',
    }
    return render(request, 'accounts/social_accounts.html', {
        'social_accounts': social_accounts,
        'form': form,
        'allauth_connected': allauth_connected,
        'available_providers': available_providers,
        'provider_labels': provider_labels,
    })

@login_required
def disconnect_social_account(request, provider):
    try:
        account = SocialAccount.objects.get(user=request.user, provider=provider)
        account.delete()
        messages.success(request, f'{provider.capitalize()} account disconnected.')
    except SocialAccount.DoesNotExist:
        messages.error(request, f'No connected {provider.capitalize()} account found.')
    return redirect('accounts:social_accounts')
