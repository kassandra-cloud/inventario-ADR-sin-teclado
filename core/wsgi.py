"""
WSGI config for core project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/howto/deployment/wsgi/
"""

import os
from django.core.wsgi import get_wsgi_application
from whitenoise import WhiteNoise
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')

# 1) Crea la app WSGI de Django
application = get_wsgi_application()

# 2) Envuelve con WhiteNoise, primero para STATIC
#    asumimos que ya has corrido `collectstatic` y hay un STATIC_ROOT
application = WhiteNoise(
    application,
    root=settings.STATIC_ROOT,
    prefix=settings.STATIC_URL  # por defecto '/static/'
)

# 3) Añade tu carpeta MEDIA
#    de modo que responda a '/media/...'
application.add_files(
    os.path.join(settings.BASE_DIR, 'media'),
    prefix=settings.MEDIA_URL  # por defecto '/media/'
)