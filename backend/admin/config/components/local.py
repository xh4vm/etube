import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

STATIC_URL = 'static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')

INTERNAL_IPS = [
    '127.0.0.1',
]
CORS_ALLOWED_ORIGINS = os.environ.get('CORS_ALLOWED_ORIGINS').split(',')

REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'config.paginators.DefaultPaginator',
    'PAGE_SIZE': 50,
}
