"""
ASGI config for web_chat project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/howto/deployment/asgi/
"""

import os
from channels.auth import AuthMiddlewareStack
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter,URLRouter
from channels.security.websocket import AllowedHostsOriginValidator
import chat.routing

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'web_chat.settings')

application = ProtocolTypeRouter({

	"websocket" : AllowedHostsOriginValidator(

		AuthMiddlewareStack(
			URLRouter(
				# app routing
				chat.routing.websocket_urlpatterns
			),
		),

	),

})
