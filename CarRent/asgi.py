"""
ASGI config for CarRent project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/howto/deployment/asgi/
"""

import os
from CarRent.conf import ENV_ID

from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', f'CarRent.env.{ENV_ID}')

application = get_asgi_application()
