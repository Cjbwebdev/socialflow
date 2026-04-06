#!/bin/bash
set -e
cd "$(dirname "$0")"

# Fix GitHub scanner corruption in settings.py
python3 << 'PYEOF'
p = "config/settings.py"
with open(p, "r") as f:
    content = f.read()

fixed = False

# Fix AUTH_USER_MODEL
if "AUTH_USER_MODEL='***'" in content:
    content = content.replace("AUTH_USER_MODEL='***'", "AUTH_USER_MODEL='accounts.User'")
    fixed = True

# Fix SECRET_KEY corruption (os.en...get pattern)
import re
# SECRET_KEY line
content = re.sub(
    r"SECRET_KEY=os\..*?'(django-insecure-change-me)'",
    "SECRET_KEY=__import__('os').environ.get('SECRET_KEY', 'django-insecure-change-me')",
    content
)
# STRIPE_SECRET_KEY
content = re.sub(
    r"STRIPE_SECRET_KEY=os\..*?''",
    "STRIPE_SECRET_KEY=__import__('os').environ.get('STRIPE_SECRET_KEY', '')",
    content
)
# STRIPE_WEBHOOK_SECRET
content = re.sub(
    r"STRIPE_WEBHOOK_SECRET=os\..*?''",
    "STRIPE_WEBHOOK_SECRET=__import__('os').environ.get('STRIPE_WEBHOOK_SECRET', '')",
    content
)
# EMAIL_HOST_PASSWORD
content = re.sub(
    r"EMAIL_HOST_PASSWORD=os\..*?''",
    "EMAIL_HOST_PASSWORD=__import__('os').environ.get('EMAIL_HOST_PASSWORD', '')",
    content
)

assert '***' not in content, f"Still has corruption!"
assert 'os.en...' not in content, f"Still has corrupted env calls!"

with open(p, "w") as f:
    f.write(content)

print("Settings patched and verified clean")
PYEOF

# Run migrations and collectstatic
python manage.py migrate --noinput
python manage.py collectstatic --noinput

# Start gunicorn
exec gunicorn config.wsgi:application --bind 0.0.0.0:$PORT --workers 2 --timeout 120
