from .base import *
from decouple import config
# Turn off debug mode for production
DEBUG = False

# Define allowed hosts (update this for your actual domain)
ALLOWED_HOSTS = ['yourdomain.com', '127.0.0.1', 'localhost']


SECRET_KEY = config('SECRET_KEY')

# Use Whitenoise for static file serving
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Enable secure settings for HTTPS
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_HSTS_SECONDS = 2592000  # 30 days
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
