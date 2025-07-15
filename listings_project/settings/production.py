from .base import *
from decouple import config
import os  # missing in your snippet

# ✅ Turn off debug mode
DEBUG = False

# ✅ Extend base.py’s INSTALLED_APPS instead of replacing it
INSTALLED_APPS += [
    # You already have the core apps in base.py, so just add production-specific ones if any
]

# ✅ Required for static files
STATIC_URL = "/static/"
STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")

# ✅ Railway will need this wildcard unless you specify your domain
ALLOWED_HOSTS = ['*']

# ✅ Production secret key
SECRET_KEY = config('SECRET_KEY')

# ✅ WhiteNoise static file handler
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# ✅ Secure settings
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_HSTS_SECONDS = 2592000  # 30 days
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
