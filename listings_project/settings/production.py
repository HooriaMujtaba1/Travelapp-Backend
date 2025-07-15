from .base import *  # Import everything from base.py
from decouple import config
import os

DEBUG = False

ALLOWED_HOSTS = ['*']

SECRET_KEY = config('SECRET_KEY')

# ✅ Static files settings
STATIC_URL = "/static/"
STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")

# ✅ Extend apps (if needed)
INSTALLED_APPS = INSTALLED_APPS + [  # Not += which may fail if not defined
    # Production-only apps (optional)
]

# ✅ WhiteNoise
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# ✅ Security
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_HSTS_SECONDS = 2592000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
