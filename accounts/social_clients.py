import json
from django.conf import settings
from requests_oauthlib import OAuth1Session
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen
from django.utils import timezone

class SocialPublishError(Exception):
    pass


def _post_json(url, payload, headers=None):
    headers = headers or {}
    if 'Content-Type' not in headers:
        headers['Content-Type'] = 'application/json'
    body = json.dumps(payload).encode('utf-8')
    request = Request(url, data=body, headers=headers, method='POST')
    try:
        with urlopen(request, timeout=20) as response:
            raw = response.read().decode('utf-8')
            return json.loads(raw) if raw else {}
    except HTTPError as exc:
        try:
            payload = exc.read().decode('utf-8')
            data = json.loads(payload)
        except Exception:
            data = {'error': payload or str(exc)}
        raise SocialPublishError(data)
    except URLError as exc:
        raise SocialPublishError(str(exc))


def _format_account_id(provider_user_id):
    if provider_user_id.isdigit():
        return f'urn:li:person:{provider_user_id}'
    return provider_user_id


def _get_access_token(account):
    if hasattr(account, 'token'):
        return account.token
    return getattr(account, 'access_token', None)


def _get_token_secret(account):
    if hasattr(account, 'token_secret'):
        return account.token_secret
    return None


def _get_provider_user_id(account):
    if hasattr(account, 'account') and hasattr(account.account, 'extra_data'):
        return account.account.extra_data.get('id') or getattr(account, 'provider_user_id', None)
    return getattr(account, 'provider_user_id', None)


def publish_post_to_provider(post, account):
    if getattr(account, 'expires_at', None) and account.expires_at < timezone.now():
        raise SocialPublishError('The access token for the account has expired.')

    provider = getattr(account, 'provider', None)
    if not provider and hasattr(account, 'account'):
        provider = account.account.provider

    if provider == 'twitter':
        return publish_twitter(post, account)
    if provider == 'linkedin':
        return publish_linkedin(post, account)
    if provider == 'instagram':
        raise SocialPublishError('Instagram posting is not supported yet for text-only content.')

    raise SocialPublishError('Unsupported social provider.')


def publish_twitter(post, account):
    access_token = _get_access_token(account)
    if not access_token:
        raise SocialPublishError('Twitter access token is missing.')

    token_secret = _get_token_secret(account)
    url = 'https://api.twitter.com/2/tweets'
    payload = {'text': post.content}

    if token_secret and settings.TWITTER_API_KEY and settings.TWITTER_API_SECRET:
        oauth = OAuth1Session(
            settings.TWITTER_API_KEY,
            client_secret=settings.TWITTER_API_SECRET,
            resource_owner_key=access_token,
            resource_owner_secret=token_secret,
        )
        response = oauth.post(url, json=payload, timeout=20)
        try:
            result = response.json()
        except ValueError:
            raise SocialPublishError('Twitter returned an unexpected response format.')
        if response.status_code >= 400 or 'errors' in result:
            raise SocialPublishError(result)
        return result

    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json',
    }
    response = _post_json(url, payload, headers=headers)
    if 'errors' in response:
        raise SocialPublishError(response)
    return response


def publish_linkedin(post, account):
    access_token = _get_access_token(account)
    if not access_token:
        raise SocialPublishError('LinkedIn access token is missing.')

    provider_user_id = _get_provider_user_id(account)
    author = _format_account_id(provider_user_id) if provider_user_id else None
    if not author or not author.startswith('urn:li:person:'):
        raise SocialPublishError('LinkedIn account ID must be a person URN or numeric person ID.')

    url = 'https://api.linkedin.com/v2/ugcPosts'
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json',
        'X-RestLi-Protocol-Version': '2.0.0',
    }
    payload = {
        'author': author,
        'lifecycleState': 'PUBLISHED',
        'specificContent': {
            'com.linkedin.ugc.ShareContent': {
                'shareCommentary': {'text': post.content},
                'shareMediaCategory': 'NONE',
            }
        },
        'visibility': {'com.linkedin.ugc.MemberNetworkVisibility': 'CONNECTIONS'},
    }
    response = _post_json(url, payload, headers=headers)
    if 'serviceErrorCode' in response or ('message' in response and 'error' in response):
        raise SocialPublishError(response)
    return response
