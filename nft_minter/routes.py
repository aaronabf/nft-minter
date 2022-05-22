from aiohttp import web
import pathlib

from .views import SiteHandler


def init_routes(app: web.Application, handler: SiteHandler) -> None:
    add_route = app.router.add_route

    app.router.add_static('/static/', path=pathlib.Path(__file__).parent / 'static', name='static')

    add_route('GET', '/', handler.index, name='index')
    add_route('POST', '/mint', handler.mint, name='mint')
