import base58
from cryptography.fernet import Fernet
import json
import os
from PIL import Image
from solana.keypair import Keypair
from solana.rpc.api import Client
import sys

from .metaplex.metaplex_api import MetaplexAPI


class MintException(Exception):
    """
    Exception during minting process.
    """
    pass


def _check_and_log(result: str) -> dict:
    """
    Checks result of API call and prints relevant information.
    """
    result = json.loads(result)
    if result['status'] != 200:
        raise MintException(f"Issue during minting process: {result}")
    print(f"tx: {result['result']}")
    return result


def upload_image_and_metadata(image: Image) -> str:
    """
    Generate a metadata file and upload both itself and the image.

    TODO! This is a quick project and storage backends typically cost money (arweave,
    s3, etc). So just going to leave out this core functionality for now...
    """
    # raise NotImplementedError
    # Random NFT for testing
    return 'https://arweave.net/1eH7bZS-6HZH4YOc8T_tGp2Rq25dlhclXJkoa6U55mM'


def _setup_wallet(api_url: str) -> (str, str):
    """
    Setups up either test wallet or returns public/private keys provided by the user.

    Ideally this could be done at startup, but for now going to leave this here.
    """
    supplied_public_key = os.getenv('WALLET_PUBLIC_KEY')
    supplied_private_key = os.getenv('WALLET_PRIVATE_KEY')
    if not supplied_public_key or not supplied_private_key:
        print('Using test wallet public and private keys')
        wallet = Keypair()
        Client(api_url).request_airdrop(wallet.public_key, int(1e9))
        public_key = str(wallet.public_key)
        private_key = base58.b58encode(wallet.seed).decode('ascii')
    else:
        print(f'Using supplied public and private keys: {supplied_public_key}')
        public_key = supplied_public_key
        private_key = supplied_private_key
    return public_key, private_key


def mint_nft(api_url: str, metadata_json_url: str) -> None:
    """
    Mints an NFT.
    """
    public_key, private_key = _setup_wallet(api_url)

    metaplex_api = MetaplexAPI(
        public_key=public_key,
        private_key=private_key,
        decryption_key=Fernet.generate_key().decode('ascii')
    )

    print('Deploy: creating new NFT token')
    result = _check_and_log(metaplex_api.deploy(api_url, 'A'*32, 'A'*10, 0))
    contract = result['contract']

    print('Topup: sending a small amount of SOL')
    _check_and_log(metaplex_api.topup(api_url, public_key))

    print('Mint: minting a token to a designated user account')
    _check_and_log(metaplex_api.mint(api_url, contract, public_key, metadata_json_url))

    print('Success')


if __name__ == '__main__':
    """
    Runnable via: python nft_minter/mint.py <api url> <metadata json url>
    """
    mint_nft(sys.argv[1], sys.argv[2])
