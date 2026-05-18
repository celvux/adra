from pathlib import Path
from decouple import config, Csv

BASE_DIR = Path(__file__).resolve().parent.parent


def _bool(val):
    return str(val).lower() in ('true', '1', 'yes')


SECRET_KEY = config('SECRET_KEY')
DEBUG = _bool(config('DEBUG', default='False'))
ALLOWED_HOSTS = config('ALLOWED_HOSTS', default='localhost,127.0.0.1', cast=Csv())
ALLOWED_HOSTS += ['.vercel.app', 'adradiallo.frondeg.co']

INSTALLED_APPS = [
    'jazzmin',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'campaign',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'adra_diallo.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'adra_diallo.wsgi.application'

_db_engine = config('DB_ENGINE', default='django.db.backends.postgresql').strip()
DATABASES = {
    'default': {
        'ENGINE':   _db_engine,
        'NAME':     config('DB_NAME',     default='adra_diallo_dev').strip(),
        'USER':     config('DB_USER',     default='postgres').strip(),
        'PASSWORD': config('DB_PASSWORD', default='postgres').strip(),
        'HOST':     config('DB_HOST',     default='localhost').strip(),
        'PORT':     config('DB_PORT',     default='5432').strip(),
        **(
            {'OPTIONS': {'connect_timeout': 10}}
            if 'postgresql' in _db_engine else {}
        ),
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

LANGUAGE_CODE = 'fr-fr'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
STATIC_ROOT = BASE_DIR / 'staticfiles'

# ─── Médias — local ou Supabase Storage (S3-compatible) ──────────────────────
USE_S3 = _bool(config('USE_S3', default='False'))

if USE_S3:
    AWS_ACCESS_KEY_ID        = config('SUPABASE_S3_KEY_ID').strip()
    AWS_SECRET_ACCESS_KEY    = config('SUPABASE_S3_SECRET').strip()
    AWS_STORAGE_BUCKET_NAME  = config('SUPABASE_BUCKET', default='media').strip()
    AWS_S3_ENDPOINT_URL      = config('SUPABASE_S3_ENDPOINT').strip()
    AWS_S3_REGION_NAME       = config('SUPABASE_S3_REGION', default='eu-west-1').strip()
    AWS_DEFAULT_ACL          = None
    AWS_S3_FILE_OVERWRITE    = False
    AWS_QUERYSTRING_AUTH     = False
    AWS_S3_SIGNATURE_VERSION = 's3v4'
    _s3_host = AWS_S3_ENDPOINT_URL.rstrip('/')
    AWS_S3_CUSTOM_DOMAIN = (
        _s3_host
        .replace('https://', '')
        .replace('/storage/v1/s3', f'/storage/v1/object/public/{AWS_STORAGE_BUCKET_NAME}')
    )
    MEDIA_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}/'
    STORAGES = {
        'default': {'BACKEND': 'storages.backends.s3boto3.S3Boto3Storage'},
        'staticfiles': {'BACKEND': 'whitenoise.storage.CompressedStaticFilesStorage'},
    }
else:
    MEDIA_URL  = '/media/'
    MEDIA_ROOT = BASE_DIR / 'media'
    STORAGES = {
        'default': {'BACKEND': 'django.core.files.storage.FileSystemStorage'},
        'staticfiles': {'BACKEND': 'whitenoise.storage.CompressedStaticFilesStorage'},
    }

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {'console': {'class': 'logging.StreamHandler'}},
    'root': {'handlers': ['console'], 'level': 'WARNING'},
    'loggers': {
        'django': {'handlers': ['console'], 'level': 'ERROR', 'propagate': False},
    },
}

# ─── JAZZMIN ──────────────────────────────────────────────────────────────────
JAZZMIN_SETTINGS = {
    "site_title": "Adra Diallo — FRONDEG",
    "site_header": "FRONDEG · Liste Nationale 2026",
    "site_brand": "FRONDEG",
    "welcome_sign": "Bienvenue dans l'espace de gestion du site de campagne d'Adra Diallo",
    "copyright": "FRONDEG — Front Démocratique de Guinée",
    "site_icon": None,
    "topmenu_links": [
        {"name": "Voir le site", "url": "/", "new_window": True},
        {"name": "Paramètres du site", "url": "/admin/campaign/sitesettings/1/change/", "icon": "fas fa-sliders-h"},
    ],
    "navigation_expanded": True,
    "order_with_respect_to": [
        "campaign",
        "campaign.SiteSettings",
        "campaign.HeroSlide",
        "campaign.KeyStat",
        "campaign.BioDimension",
        "campaign.TimelineStep",
        "campaign.ProgramAxis",
        "campaign.Commitment",
        "campaign.Publication",
        "campaign.ComparativeAnalysis",
        "campaign.ComparisonPoint",
        "campaign.NewsArticle",
        "auth",
    ],
    "icons": {
        "auth":                         "fas fa-users-cog",
        "auth.user":                    "fas fa-user",
        "auth.Group":                   "fas fa-users",
        "campaign.SiteSettings":        "fas fa-sliders-h",
        "campaign.HeroSlide":           "fas fa-images",
        "campaign.KeyStat":             "fas fa-chart-bar",
        "campaign.BioDimension":        "fas fa-id-card",
        "campaign.TimelineStep":        "fas fa-history",
        "campaign.ProgramAxis":         "fas fa-tasks",
        "campaign.Commitment":          "fas fa-handshake",
        "campaign.Publication":         "fas fa-graduation-cap",
        "campaign.ComparativeAnalysis": "fas fa-balance-scale",
        "campaign.ComparisonPoint":     "fas fa-columns",
        "campaign.NewsArticle":         "fas fa-newspaper",
    },
    "default_icon_parents": "fas fa-folder",
    "default_icon_children": "fas fa-circle",
    "hide_apps": [],
    "hide_models": [],
    "theme": "flatly",
    "dark_mode_theme": None,
    "custom_links": {
        "campaign": [{
            "name": "Voir le site public",
            "url": "/",
            "icon": "fas fa-eye",
            "new_window": True,
        }]
    },
}

JAZZMIN_UI_TWEAKS = {
    "navbar_small_text": False,
    "footer_small_text": False,
    "body_small_text": False,
    "brand_small_text": False,
    "brand_colour": "navbar-dark",
    "accent": "accent-primary",
    "navbar": "navbar-white navbar-light",
    "no_navbar_border": False,
    "navbar_fixed": True,
    "layout_boxed": False,
    "footer_fixed": False,
    "sidebar_fixed": True,
    "sidebar": "sidebar-dark-primary",
    "sidebar_nav_small_text": False,
    "sidebar_disable_expand": False,
    "sidebar_nav_child_indent": True,
    "sidebar_nav_compact_style": False,
    "sidebar_nav_legacy_style": False,
    "sidebar_nav_flat_style": False,
    "theme": "flatly",
    "button_classes": {
        "primary": "btn-primary",
        "secondary": "btn-secondary",
        "info": "btn-info",
        "warning": "btn-warning",
        "danger": "btn-danger",
        "success": "btn-success",
    },
}
