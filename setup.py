from setuptools import find_packages, setup


version = 'dev'
install_requires = [
    'aiohttp',
    'aiohttp_jinja2',
    'base58',
    'cryptography',
    'dacite',
    'Pillow',
    'solana',
    'trafaret_config',
]


setup(
    name='nft-minter',
    version=version,
    description='Mints NFT',
    platforms=['POSIX'],
    packages=find_packages(),
    package_data={'': ['config/*.*']},
    include_package_data=True,
    install_requires=install_requires,
    zip_safe=False,
)
