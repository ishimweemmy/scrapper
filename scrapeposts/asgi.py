import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.security.websocket import AllowedHostsOriginValidator
import scrape.routing 

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "scrapeposts.settings")
django_asgi_app = get_asgi_application()

application = ProtocolTypeRouter({
    "http": django_asgi_app,
    "websocket": AllowedHostsOriginValidator(URLRouter(scrape.routing.websocket_urlpatterns)),
})
