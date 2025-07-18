from .base import *  # Import everything from base.py
from decouple import config
import os
import dj_database_url

DEBUG = False

ALLOWED_HOSTS = ['*']  # You can restrict this to your Railway domain for more security

# ✅ Load SECRET_KEY securely
SECRET_KEY = config('SECRET_KEY')
print("✅ SECRET_KEY Loaded:", SECRET_KEY[:5])  # for debugging

# ✅ PostgreSQL Database Configuration
DATABASES = {
    'default': dj_database_url.config(
        default=config('DATABASE_URL'),  # From Railway: postgresql://...
        conn_max_age=600,
        ssl_require=True
    )
}

# ✅ Static files settings
STATIC_URL = "/static/"
STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")

# ✅ WhiteNoise configuration for serving static files
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# ✅ Security settings for HTTPS
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_HSTS_SECONDS = 2592000  # 30 days
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
