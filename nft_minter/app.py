from aiohttp import web
import aiohttp_jinja2
import asyncio
import jinja2
from pathlib import Path

from .config import Config, get_config, init_config
from .routes import init_routes
from .views import SiteHandler


def init_jinja2(app: web.Application) -> None:
    aiohttp_jinja2.setup(
        app,
        loader=jinja2.FileSystemLoader(Path(__file__).parent / 'templates')
    )


async def init_app(conf: Config) -> web.Application:
    app = web.Application(client_max_size=conf.image.max_image_size_mb)
    init_config(app, conf)
    init_jinja2(app)
    handler = SiteHandler(conf)
    init_routes(app, handler)
    return app


def main() -> None:
    conf = get_config()
    loop = asyncio.get_event_loop()
    app = loop.run_until_complete(init_app(conf))
    web.run_app(app, host=conf.app.host, port=conf.app.port)
