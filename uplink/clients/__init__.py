"""
This package defines an adapter layer for handling requests built by
Uplink's high-level, declarative API with existing HTTP clients
(`requests`, `asyncio`, etc.).

We refer to this layer as the backend, as these adapters handle the
actual client behavior (i.e., making a request to a server).

Note:
    At some point, we may want to expose this layer to the user, so
    they can create custom adapters.
"""
# Standard library imports
import inspect

# Local imports
from uplink.clients import interfaces, register
from uplink.clients.register import DEFAULT_CLIENT, get_client
from uplink.clients.requests_ import RequestsClient
from uplink.clients.twisted_ import TwistedClient


@register.handler
def _client_class_handler(key):
    if inspect.isclass(key) and issubclass(key, interfaces.HttpClientAdapter):
        return key()


try:
    from uplink.clients.aiohttp_ import AiohttpClient
except (ImportError, SyntaxError) as error:  # pragma: no cover
    from uplink.clients import interfaces

    class AiohttpClient(interfaces.HttpClientAdapter):
        def __init__(self, *args, **kwargs):
            raise NotImplementedError(
                "Failed to load `aiohttp` client: you may be using a version "
                "of Python below 3.3. `aiohttp` requires Python 3.4+."
            )

        def create_request(self):
            pass

__all__ = [
    "RequestsClient",
    "AiohttpClient",
    "TwistedClient",
]

register.set_default_client(RequestsClient)
