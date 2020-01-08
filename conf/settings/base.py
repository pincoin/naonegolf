import json
import os

from . import BASE_DIR

# Secret settings
secret = json.loads(open(os.path.join(BASE_DIR, 'secret.json')).read())

SECRET_KEY = secret['SECRET_KEY']
ALLOWED_HOSTS = secret['ALLOWED_HOSTS']
DATABASES = secret['DATABASES']

EMAIL_HOST = secret['EMAIL_HOST']
EMAIL_HOST_USER = secret['EMAIL_HOST_USER']
EMAIL_HOST_PASSWORD = secret['EMAIL_HOST_PASSWORD']
EMAIL_PORT = secret['EMAIL_PORT']
EMAIL_USE_TLS = secret['EMAIL_USE_TLS']
EMAIL_NO_REPLY = secret['EMAIL_NO_REPLY']
EMAIL_CUSTOMER_SERVICE = secret['EMAIL_CUSTOMER_SERVICE']

LINE_NOTIFY_ACCESS_TOKEN = secret['LINE_NOTIFY_ACCESS_TOKEN']

CELERY_BROKER_URL = secret['CELERY_BROKER_URL']

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'allauth',
    'allauth.account',
    # 'allauth.socialaccount',
    # 'allauth.socialaccount.providers.facebook',
    # 'allauth.socialaccount.providers.kakao',
    # 'member.socialaccount.providers.line',
]

INSTALLED_APPS += [
    'golf',
    'windmill',
    'member',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware', # i18n
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'conf.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, 'conf', 'templates'),
            os.path.join(BASE_DIR, 'member', 'templates'),
            os.path.join(BASE_DIR, 'golf', 'templates'),
            os.path.join(BASE_DIR, 'windmill', 'templates'),
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'conf.wsgi.application'

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator', },
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator', },
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator', },
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator', },
]

AUTHENTICATION_BACKENDS = (
    # Needed to login by username in Django admin, regardless of `allauth`
    'django.contrib.auth.backends.ModelBackend',

    # `allauth` specific authentication methods, such as login by e-mail
    'allauth.account.auth_backends.AuthenticationBackend',
)

# for django-allauth
SITE_ID = 1

# django.contrib.auth settings for allauth
PASSWORD_RESET_TIMEOUT_DAYS = 1  # default=3
LOGIN_URL = '/accounts/login/'  # default=/accounts/login/
LOGOUT_URL = '/accounts/logout/'  # default=/accounts/logout/
LOGIN_REDIRECT_URL = '/'  # default=/accounts/profile/
# LOGOUT_REDIRECT_URL = '/'

# django-allauth
DEFAULT_FROM_EMAIL = EMAIL_NO_REPLY
# ACCOUNT_ADAPTER = 'member.adapters.MyAccountAdapter'
ACCOUNT_AUTHENTICATION_METHOD = 'email'
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_EMAIL_VERIFICATION = 'mandatory'
ACCOUNT_LOGIN_ATTEMPTS_LIMIT = 5
ACCOUNT_LOGIN_ATTEMPTS_TIMEOUT = 300
# ACCOUNT_SIGNUP_FORM_CLASS = 'member.forms2.MemberSignupForm'
ACCOUNT_LOGOUT_ON_PASSWORD_CHANGE = True  # default=False
SOCIALACCOUNT_AUTO_SIGNUP = False

# Social providers for django-allauth
# Each key has an empty dictionary value that will eventually contain provider specific configuration options by admin
SOCIALACCOUNT_PROVIDERS = {
    'facebook': {},
    'kakao': {},
    'line': {
        'SCOPE': [
            'profile',
            'openid',
            'email',
        ],
    },
}
