# SocialFlow — Multi-Platform Scheduling

Schedule posts to Twitter/X, LinkedIn, and Instagram from one dashboard.

## Setup
```bash
cd socialflow
pip install -r requirements.txt
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

## Features
- Write once, publish everywhere
- Multi-platform scheduling
- User auth + billing
- Admin dashboard

## Social OAuth setup
1. Create a superuser and log into Django admin at `/admin/`.
2. Add `Social Applications` for Twitter/X and LinkedIn.
3. Set the callback URL for each app to `http://127.0.0.1:8000/accounts/twitter_oauth2/login/callback/` and `http://127.0.0.1:8000/accounts/linkedin_oauth2/login/callback/`.
4. Configure your environment variables:
   - `TWITTER_CLIENT_ID`
   - `TWITTER_CLIENT_SECRET`
   - `LINKEDIN_CLIENT_ID`
   - `LINKEDIN_CLIENT_SECRET`
5. Visit `/social-accounts/` and click the provider connect buttons.
