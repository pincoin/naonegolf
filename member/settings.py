from django.conf import settings

DISALLOWED_EMAIL_DOMAIN = getattr(settings, 'DISALLOWED_EMAIL_DOMAIN', (
    'qq.com', '163.com', '126.com', '188.com', 'yeah.net', 'sina.com'
))
