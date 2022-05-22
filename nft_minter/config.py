from aiohttp import web
import argparse
from dacite import from_dict
from dataclasses import dataclass
import pathlib
import trafaret
from trafaret_config import commandline


CONFIG_PATH = pathlib.Path(__file__).parent.parent / 'config' / 'config.yaml'


CONFIG_VALIDATION = trafaret.Dict({
    trafaret.Key('app'): trafaret.Dict({
        trafaret.Key('host'): trafaret.String(),
        trafaret.Key('port'): trafaret.Int[0: 2 ** 16],
    }),
    trafaret.Key('image'): trafaret.Dict({
        trafaret.Key('max_image_size_mb'): trafaret.Int[1: 32],
        trafaret.Key('pixel_count'): trafaret.Int[1: 2048],
    }),
    trafaret.Key('crypto'): trafaret.Dict({
        trafaret.Key('enabled'): trafaret.Bool(),
        trafaret.Key('api'): trafaret.String(),
    }),
})


@dataclass(frozen=True)
class AppConfig:
    host: str
    port: int


@dataclass(frozen=True)
class ImageConfig:
    max_image_size_mb: int
    pixel_count: int


@dataclass(frozen=True)
class CryptoConfig:
    enabled: bool
    api: str


@dataclass(frozen=True)
class Config:
    app: AppConfig
    image: ImageConfig
    crypto: CryptoConfig


def _apply_config_transformations(conf: dict) -> None:
    # Convert megabytes field to bytes
    conf['image']['max_image_size_mb'] *= 1024 * 1024


def get_config() -> Config:
    ap = argparse.ArgumentParser()
    commandline.standard_argparse_options(ap, default_config=CONFIG_PATH)
    options = ap.parse_args()
    config_dict = commandline.config_from_options(options, CONFIG_VALIDATION)
    _apply_config_transformations(config_dict)
    return from_dict(data_class=Config, data=config_dict)


def init_config(app: web.Application, config: Config) -> None:
    app['config'] = config
