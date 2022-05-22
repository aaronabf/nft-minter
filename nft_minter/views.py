from aiohttp import web
import aiohttp_jinja2
import io
from PIL import Image
from typing import Dict

from .art import transform_image
from .config import Config
from .mint import mint_nft, upload_image_and_metadata


class SiteHandler:
    def __init__(self, conf: Config) -> None:
        self._conf = conf

    @aiohttp_jinja2.template('index.html')
    async def index(self, request: web.Request) -> Dict[str, str]:
        return {}

    async def mint(self, request: web.Request) -> web.Response:
        form = await request.post()

        # Transform image
        raw_image = form['file'].file.read()
        original_image = Image.open(io.BytesIO(raw_image))
        new_image = transform_image(original_image, self._conf)

        # Mint NFT
        if self._conf.crypto.enabled:
            url = upload_image_and_metadata(new_image)
            mint_nft(self._conf.crypto.api, url)

        # Return result to client
        image_stream = io.BytesIO()
        new_image.save(image_stream, format='png')
        return web.Response(
            body=image_stream.getvalue(),
            headers={'Content-type': 'image/png'},
        )
