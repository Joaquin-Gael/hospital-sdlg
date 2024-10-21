from pathlib import Path
import os, dj_database_url, sys
from django.urls import reverse_lazy
from datetime import timedelta

GOOGLE_CLIENT_ID = '82678305256-58rv9un7jfe17etgp69f7d8lucqetukh.apps.googleusercontent.com'
GOOGLE_CLIENT_SECRET = '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'
CALLBACK_URL = reverse_lazy('oauth_callback')

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'hospitalsdlg@gmail.com'
EMAIL_HOST_PASSWORD = 'yzle flnf eepj nkcj'

RECAPTCHA_PUBLIC_KEY  = '6LdK6jcqAAAAANLSDYCNgrMlwX8pR6FtHBT9k1Ef'
RECAPTCHA_PRIVATE_KEY = '6LdK6jcqAAAAAFi6nxjs0wkvpM57q3NNwIhDgs9P'
RECAPTCHA_USE_SSL = False


JWT_HASH = "HS256"
FERNET_KEY:str = 'bp3-2Zt5nUsRlXq82F-_m0apVBvkyJpwWNP3UIOIl8c='

DB_PROD = True

JAZZMIN_SETTINGS = {
    "site_title":"Hospital SDLG Admin Panel",
    "site_header":"Hospital SDLG Admin Panel",
    "show_sidebar":True,
    "icons": {
        "auth": "fas fa-users-cog",
        "auth.User": "fas fa-user",
        "auth.Group": "fas fa-users",
        "user.Usuarios": "fas fa-user",
        "security.BlackListTokens": "fas fa-lock",
        "blog.Testimonios": "fas fa-newspaper",
        "turnero.Turnos": "fas fa-calendar-alt",
        "medicos.Medicos": "fas fa-user-md",
        "turnero.Citas": "fas fa-calendar-alt",
        "turnero.CajaTurnero": "fas fa-money-bill-wave",
        "turnero.DetallesCaja": "fas fa-money-bill-wave",
        "security.SessionTokens": "fas fa-eye-slash",
        "medicos.Ubicaciones":"fas fa-map-pin",
        "medicos.Departamentos":"fas fa-building",
        "medicos.Especialidades":"fas fa-stethoscope",
        "medicos.Servicios":"fas fa-stethoscope",
        "medicos.Horario_medicos":"fas fa-calendar-alt",
        "blog.News":"fas fa-newspaper",
        "account.EmailAddress":"fas fa-at"
    },
    "custom_links": {
        "Configuración": [
            {
                "title": "API Documentation",
                "url": "/API/security/swagger/",
                "icon": "fas fa-book",
            },
        ],
    },
    "welcome_sign": "Bienvenido al panel de administración de Hospital SDLG",
    "changeform_format": "carousel",
    "related_modal_active": True,

}

JAZZMIN_UI_TWEAKS = {
    "theme": "lux",
}

TINYMCE_DEFAULT_CONFIG = {
    'theme': 'silver',
    'height': 300,
    'width': '100%',
    'plugins': 'advlist autolink lists link image charmap print preview',
    'toolbar': 'undo redo | styleselect | bold italic | alignleft aligncenter alignright | bullist numlist outdent indent | link image',
}


BASE_DIR = Path(__file__).resolve().parent.parent

sys.path.append(os.path.join(BASE_DIR, 'tests'))

SECRET_KEY = os.environ.get('SECRET_KEY', default='django-insecure-^=6-_k)oh!n9-fpcd1qd0rf(!8y2!!8cc*so1if(!*ydv@*_dc')

DEBUG = 'RENDER' not in os.environ

ALLOWED_HOSTS = ['*']

APPEND_SLASH = True 

if not DEBUG:
    ALLOWED_HOSTS = []
    RENDER_EXTERNAL_HOSTNAME = os.environ.get('RENDER_EXTERNAL_HOSTNAME')
    if RENDER_EXTERNAL_HOSTNAME:
        ALLOWED_HOSTS.append(os.environ.get('RENDER_EXTERNAL_HOSTNAME'))


HOSPITAL_APPS = [
    'blog',
    'turnero',
    'user',
    'medicos',
    'API',
    'security'
]

TIRDSHPARTY_APPS = [
    'rest_framework',
    'django_recaptcha',
    'crispy_forms', 
    'drf_yasg',
    'rest_framework_simplejwt',
    'adrf',
    'channels'
    'tinymce'
    #'ckeditor'
]

DJANGO_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites'
]

INSTALLED_APPS = DJANGO_APPS + HOSPITAL_APPS + TIRDSHPARTY_APPS

INSTALLED_APPS.insert(0, 'jazzmin')


INTERNAL_IPS = [
    '127.0.0.1',
]

if DEBUG:
    CSRF_TRUSTED_ORIGINS = [
        'http://localhost:8000',
        'http://127.0.0.1:8000',
    ]
else:
    CSRF_TRUSTED_ORIGINS = []

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'user.middleware.UserDataMiddleware',
]

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',  # Backend por defecto
)

if DEBUG:
    INSTALLED_APPS.append('debug_toolbar')
    MIDDLEWARE.insert(0, 'debug_toolbar.middleware.DebugToolbarMiddleware')

DEBUG_TOOLBAR_PANELS = [
    'debug_toolbar.panels.history.HistoryPanel',
    'debug_toolbar.panels.versions.VersionsPanel',
    'debug_toolbar.panels.timer.TimerPanel',
    'debug_toolbar.panels.settings.SettingsPanel',
    'debug_toolbar.panels.headers.HeadersPanel',
    'debug_toolbar.panels.request.RequestPanel',
    'debug_toolbar.panels.sql.SQLPanel',
    'debug_toolbar.panels.staticfiles.StaticFilesPanel',
    'debug_toolbar.panels.templates.TemplatesPanel',
    'debug_toolbar.panels.alerts.AlertsPanel',
    'debug_toolbar.panels.cache.CachePanel',
    'debug_toolbar.panels.signals.SignalsPanel',
    'debug_toolbar.panels.redirects.RedirectsPanel',
    'debug_toolbar.panels.profiling.ProfilingPanel',
]

ROOT_URLCONF = 'mysite.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            f'{BASE_DIR}/templates'
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'user.context_processors.handler_user_data_redirection',
            ],
        },
    },
]

ASGI_APPLICATION = 'mysite.asgi.application'


DATABASES = {
    'default': dj_database_url.config(
        default=f'sqlite:///{BASE_DIR / "db.sqlite3"}',
        conn_max_age=800
    )
}

if DB_PROD:
    DATABASES['default'] = dj_database_url.parse("postgresql://postgres:kmIDiyNAGfEYoXnyfMaIcPkadTngCKDg@junction.proxy.rlwy.net:23151/railway")


AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


AUTH_USER_MODEL = 'user.Usuarios'

LANGUAGE_CODE = 'es-ar'

TIME_ZONE = 'America/Argentina/Buenos_Aires'

USE_I18N = True

USE_TZ = True

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'mediafiles')

LOGIN_URL = reverse_lazy('LoginUser')

BOOSTRAP_ROOT = Path(__file__).resolve().parent.parent.parent / 'node_modules/'

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_DIRS = [
    f'{BASE_DIR}/static',
    f'{BOOSTRAP_ROOT}/bootstrap',
    f'{BOOSTRAP_ROOT}/flatpickr',
    f'{BOOSTRAP_ROOT}/@popperjs/core',
    f'{BOOSTRAP_ROOT}/jquery',
]

if not DEBUG:
    STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.TokenAuthentication',
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
        'rest_framework.permissions.IsAdminUser',
    ],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 10,
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer',
        'rest_framework.renderers.BrowsableAPIRenderer'
    ],
}


SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=5),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=1),
    "ROTATE_REFRESH_TOKENS": True,
    "BLACKLIST_AFTER_ROTATION": True,
    "ALGORITHM": JWT_HASH,
    "SIGNING_KEY": SECRET_KEY,
    "VERIFYING_KEY": "",
    "AUDIENCE": None,
    "ISSUER": None,
    "JSON_ENCODER": None,
    "JWK_URL": None,
    "LEEWAY": 0,

    "AUTH_HEADER_TYPES": ("Bearer",),
    "AUTH_HEADER_NAME": "HTTP_AUTHORIZATION",
    "USER_ID_FIELD": "userID",
    "USER_ID_CLAIM": "user_id",
    "USER_AUTHENTICATION_RULE": "rest_framework_simplejwt.authentication.default_user_authentication_rule",

    "AUTH_TOKEN_CLASSES": ("rest_framework_simplejwt.tokens.AccessToken",),
    "TOKEN_TYPE_CLAIM": "token_type",
    "TOKEN_USER_CLASS": "rest_framework_simplejwt.models.TokenUser",

    "JTI_CLAIM": "jti",

    "SLIDING_TOKEN_REFRESH_EXP_CLAIM": "refresh_exp",
    "SLIDING_TOKEN_LIFETIME": timedelta(minutes=5),
    "SLIDING_TOKEN_REFRESH_LIFETIME": timedelta(days=1),

    "TOKEN_OBTAIN_SERIALIZER": "security.serializers.SecurityTokenSerializer",
    "TOKEN_REFRESH_SERIALIZER": "rest_framework_simplejwt.serializers.TokenRefreshSerializer",
    "TOKEN_VERIFY_SERIALIZER": "rest_framework_simplejwt.serializers.TokenVerifySerializer",
    "TOKEN_BLACKLIST_SERIALIZER": "security.serializers.TokenBlacklistRedisSerializer",
    "SLIDING_TOKEN_OBTAIN_SERIALIZER": "rest_framework_simplejwt.serializers.TokenObtainSlidingSerializer",
    "SLIDING_TOKEN_REFRESH_SERIALIZER": "rest_framework_simplejwt.serializers.TokenRefreshSlidingSerializer",
}