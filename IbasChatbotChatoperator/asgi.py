"""
ASGI config for IbasChatbotChatoperator project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/howto/deployment/asgi/
"""
import os
import django
from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application
from channels.auth import AuthMiddlewareStack
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "IbasChatbotChatoperator.settings")
django.setup()

# TODO: Import the routing file(s) & store the import as tuple
import home.routing as home_r
import staffApp.routing as stff_r
from django.conf import settings

"""
Concept of adding multiple routing files: 
https://stackoverflow.com/questions/68837988/how-use-more-than-one-routings-file-in-django-channels
"""

django_asgi_app = get_asgi_application()

#os.environ.setdefault("DJANGO_SETTINGS_MODULE", "IbasChatbotChatoperator.settings")
#settings.configure()
#django.setup()

application = ProtocolTypeRouter(
    {
        # Just HTTP for now. (We can add other protocols later.)
        "http": get_asgi_application(),
        #"http": django_asgi_app,     # TESTING
        'websocket': AuthMiddlewareStack(
            URLRouter(
                home_r.websocket_urlpatterns +
                stff_r.websocket_urlpatterns
            ),
        ),
    }
)

