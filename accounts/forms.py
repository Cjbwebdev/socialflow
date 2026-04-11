from django import forms
from .models import SocialAccount

class SocialAccountForm(forms.ModelForm):
    expires_at = forms.DateTimeField(
        required=False,
        widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        help_text='Optional expiry date for the token if available.',
    )

    class Meta:
        model = SocialAccount
        fields = ['provider', 'provider_user_id', 'access_token', 'refresh_token', 'expires_at']
        widgets = {
            'provider': forms.Select(attrs={'class': 'form-select'}),
            'provider_user_id': forms.TextInput(attrs={'placeholder': 'Provider user ID or URN'}),
            'access_token': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Paste your access token here'}),
            'refresh_token': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Paste refresh token if available'}),
        }
        help_texts = {
            'access_token': 'A valid OAuth access token for the selected provider.',
            'provider_user_id': 'LinkedIn: person URN (e.g. urn:li:person:xxxx); Twitter: user ID; Instagram: IG user ID.',
        }
