# NFT Minter

Transforms uploaded image into pixel art and mints resulting image as an NFT on Solona.

Configured to use Solana Devnet server.

This is a quick project to play around with the tech. No promises on its reliability.

---

System Requirements

- macOS or Linux
- Python 3.+

Setup


```bash
git clone git@github.com:aaronabf/nft-minter.git
cd nft-minter
python3 -m venv .venv
source .venv/bin/activate
pip install -e .
```

Run against a test wallet

```bash
python -m nft_minter
```

Run against a real wallet

```bash
WALLET_PRIVATE_KEY=put_your_private_key_here WALLET_PUBLIC_KEY=put_your_public_key_here python -m nft_minter
````
