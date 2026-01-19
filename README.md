# Ethereum Wallet Toolkit

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Ethereum Foundation](https://img.shields.io/badge/Ethereum-Foundation%20Libraries-3C3C3D.svg)](https://ethereum.org/)

> **Secure, auditable Python CLI for Ethereum wallet generation, vanity addresses, BIP39 mnemonics, HD wallets, and message signing — using only official Ethereum Foundation libraries.**

### 🔑 Key Features

- **Wallet Generation** — Random wallets with cryptographically secure randomness
- **BIP39 Mnemonics** — 12/15/18/21/24-word seed phrases in multiple languages
- **HD Wallets (BIP32/BIP44)** — Derive multiple addresses from one seed
- **Vanity Addresses** — Generate addresses with custom prefixes/suffixes
- **Message Signing** — EIP-191 personal_sign with verification
- **Contract Addresses** — Predict CREATE and CREATE2 deployment addresses
- **100% Offline** — No network calls, fully air-gappable
- **Auditable Code** — Single-file Python, easy to review

---

## DISCLAIMER - EDUCATIONAL PURPOSES ONLY - NO LIABILITY

**THIS SOFTWARE IS PROVIDED FOR EDUCATIONAL AND RESEARCH PURPOSES ONLY.**

**DO NOT USE WITH REAL FUNDS. DO NOT USE IN PRODUCTION.**

The author(s) accept **NO LIABILITY** for any damages, losses, or consequences arising from the use of this software. By using this software, you acknowledge that you are solely responsible for your actions and any outcomes.

This software is provided "AS IS" without warranty of any kind. The author(s) make no guarantees about the security, correctness, or fitness for any purpose.

**ALWAYS:**
- Audit the code yourself before any use
- Use hardware wallets for real funds
- Never use generated keys for real assets
- Understand that vanity address generation has inherent risks

---

A comprehensive Python CLI toolkit for Ethereum wallet operations using official Ethereum Foundation libraries.

## Security

This toolkit uses **only official, audited libraries from the Ethereum Foundation**. No third-party cryptographic code.

| Library | Repository | Maintainer | Purpose |
|---------|------------|------------|---------|
| [eth-account](https://github.com/ethereum/eth-account) | ethereum/eth-account | Ethereum Foundation | Key generation, signing, HD wallets |
| [eth-keys](https://github.com/ethereum/eth-keys) | ethereum/eth-keys | Ethereum Foundation | ECDSA operations |
| [eth-rlp](https://github.com/ethereum/eth-rlp) | ethereum/eth-rlp | Ethereum Foundation | RLP encoding |
| [eth-utils](https://github.com/ethereum/eth-utils) | ethereum/eth-utils | Ethereum Foundation | Utility functions |
| [rlp](https://github.com/ethereum/pyrlp) | ethereum/pyrlp | Ethereum Foundation | Contract address calculation |

All cryptographic operations are handled by these official packages. The toolkit code itself only provides the CLI interface and pattern matching logic.

The code is fully auditable - review it yourself before use.

## Security Best Practices

1. **Run offline** - Disconnect from the internet when generating wallets
2. **Audit the code** - It's open source, verify it yourself
3. **Never share private keys or mnemonics**
4. **Store secrets securely** - Use hardware wallets for significant funds
5. **Do not use online generators** - They could steal your keys

### IMPORTANT WARNING

**USE THIS TOOLKIT AT YOUR OWN RISK.** This is provided for educational and research purposes only. Do not use for high-value wallets.

In September 2022, **Wintermute lost $160 million** due to a vulnerability in the "Profanity" vanity generator, which used weak randomness (4-byte seed reducing keyspace from 2^256 to 2^32).

This toolkit avoids the specific Profanity vulnerability by:
- Using OS-level CSPRNG via `eth-account` (not incremental seed-based generation)
- Each wallet uses fresh, cryptographically secure randomness
- Based on audited Ethereum Foundation libraries

**However, this does NOT guarantee safety.** Vanity address generation for EOAs carries inherent risks. Always audit the code yourself and understand what you're doing before any use.

See [docs/SECURITY.md](docs/SECURITY.md) for detailed security analysis and [docs/VANITY_RESOURCES.md](docs/VANITY_RESOURCES.md) for research references.

### Further Reading

- [Web3.py Patterns: Address Mining](https://snakecharmers.ethereum.org/web3-py-patterns-address-mining/) - Ethereum Foundation's Snake Charmers blog explaining vanity address concepts

## Installation

```bash
# Clone the repository
git clone https://github.com/nirholas/ethereum-wallet-toolkit.git
cd ethereum-wallet-toolkit

# Create virtual environment (recommended)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

## Features

### 1. Generate Random Wallet

```bash
# Simple random wallet
python eth_toolkit.py generate

# With BIP39 mnemonic (12/15/18/21/24 words)
python eth_toolkit.py generate --mnemonic
python eth_toolkit.py generate --mnemonic --words 24

# With passphrase (extra security)
python eth_toolkit.py generate --mnemonic --passphrase "my secret"

# Different language mnemonics
python eth_toolkit.py generate --mnemonic --language spanish

# Save to file
python eth_toolkit.py generate --mnemonic --output wallet.json
```

### 2. Generate Vanity Address

```bash
# Prefix matching (address starts with)
python eth_toolkit.py vanity --prefix dead
python eth_toolkit.py vanity --prefix abc123

# Suffix matching (address ends with)
python eth_toolkit.py vanity --suffix beef

# Both prefix and suffix
python eth_toolkit.py vanity --prefix dead --suffix beef

# Contains pattern anywhere
python eth_toolkit.py vanity --contains cafe

# Case-sensitive (EIP-55 checksum)
python eth_toolkit.py vanity --prefix ABC --case-sensitive

# Letters only (a-f)
python eth_toolkit.py vanity --letters

# Numbers only (0-9)
python eth_toolkit.py vanity --numbers

# Mirror pattern
python eth_toolkit.py vanity --mirror

# Multi-threaded (faster)
python eth_toolkit.py vanity --prefix dead --threads 8

# Generate multiple addresses
python eth_toolkit.py vanity --prefix ab --count 5 --output vanity_wallets.json

# Quiet mode (minimal output)
python eth_toolkit.py vanity --prefix abc --quiet
```

### 3. Restore Wallet

```bash
# From mnemonic
python eth_toolkit.py restore --mnemonic word1 word2 word3 word4 word5 word6 word7 word8 word9 word10 word11 word12

# From mnemonic with passphrase
python eth_toolkit.py restore --mnemonic word1 word2 ... --passphrase "secret"

# From mnemonic with custom derivation path
python eth_toolkit.py restore --mnemonic word1 word2 ... --path "m/44'/60'/0'/0/5"

# From private key
python eth_toolkit.py restore --key 0x1234...
```

### 4. Derive Multiple Accounts

```bash
# Derive 10 accounts from mnemonic
python eth_toolkit.py derive --mnemonic word1 word2 ... --count 10

# Show private keys
python eth_toolkit.py derive --mnemonic word1 word2 ... --count 5 --verbose

# Custom base path
python eth_toolkit.py derive --mnemonic word1 word2 ... --base-path "m/44'/60'/1'/0"
```

### 5. Sign Messages

```bash
# Sign a message
python eth_toolkit.py sign --message "Hello, Ethereum!" --key 0x1234...

# Verbose output (show r, s, v)
python eth_toolkit.py sign --message "Hello" --key 0x1234... --verbose
```

### 6. Verify Signatures

```bash
# Verify a signed message
python eth_toolkit.py verify \
  --message "Hello, Ethereum!" \
  --signature 0xabcd... \
  --address 0x1234...
```

### 7. Validate Address/Key

```bash
# Validate address format
python eth_toolkit.py validate --address 0x1234...

# Validate private key format
python eth_toolkit.py validate --key 0xabcd...

# Verify key matches address
python eth_toolkit.py validate --address 0x1234... --key 0xabcd...
```

### 8. Keystore Operations

Encrypt and decrypt Web3 Secret Storage (V3) keystores compatible with MetaMask, Geth, and other wallets.

```bash
# Encrypt private key to keystore
python eth_toolkit.py keystore --encrypt --key 0x1234... --password secret --output wallet.json

# Decrypt keystore file
python eth_toolkit.py keystore --decrypt --file wallet.json --password secret

# Choose KDF algorithm (scrypt or pbkdf2)
python eth_toolkit.py keystore --encrypt --key 0x1234... --password secret --kdf pbkdf2 --output wallet.json
```

### 9. Offline Transaction Signing

Create and sign transactions without an internet connection. Supports both legacy and EIP-1559 transactions.

```bash
# Sign simple ETH transfer (EIP-1559)
python eth_toolkit.py transaction --to 0x... --ether 1.5 --nonce 0 --key 0x...

# Sign with specific gas parameters
python eth_toolkit.py transaction --to 0x... --ether 0.5 --nonce 5 \
  --max-fee 30000000000 --priority-fee 2000000000 --key 0x...

# Sign legacy transaction
python eth_toolkit.py transaction --to 0x... --value 1000000000000000000 --nonce 0 \
  --gas-price 20000000000 --key 0x...

# Different networks (chain IDs)
python eth_toolkit.py transaction --to 0x... --ether 1 --nonce 0 --chain-id 137 --key 0x...
```

### 10. EIP-712 Typed Data Signing

Sign structured data for DeFi permits, DEX orders, and meta-transactions.

```bash
# Sign typed data from JSON file
python eth_toolkit.py typed-data --sign --file permit.json --key 0x...

# Verify typed data signature
python eth_toolkit.py typed-data --verify --file permit.json --signature 0x... --address 0x...
```

## Standalone Modules

Each feature is also available as a standalone Python script:

| Module | Description | Usage |
|--------|-------------|-------|
| [wallet.py](wallet.py) | Wallet generation/restoration | `python wallet.py generate --mnemonic` |
| [keystore.py](keystore.py) | Keystore encrypt/decrypt | `python keystore.py encrypt --key 0x...` |
| [sign.py](sign.py) | Message signing | `python sign.py sign --message "Hello" --key 0x...` |
| [transaction.py](transaction.py) | Transaction signing | `python transaction.py sign --to 0x... --ether 1 --nonce 0 --key 0x...` |
| [typed_data.py](typed_data.py) | EIP-712 typed data | `python typed_data.py sign --file permit.json --key 0x...` |
| [validate.py](validate.py) | Address/key validation | `python validate.py address --address 0x...` |
| [vanity.py](vanity.py) | Vanity address generation | `python vanity.py --prefix abc` |

## Legacy Vanity Generator

The original simple vanity generator is still available:

```bash
python vanity.py --prefix abc --suffix 123 --threads 4
```

## Vanity Address Time Estimates

| Characters | Difficulty | Est. Time (8 cores) |
|------------|------------|---------------------|
| 1 | 1 in 16 | Instant |
| 2 | 1 in 256 | < 1 second |
| 3 | 1 in 4,096 | ~1 second |
| 4 | 1 in 65,536 | ~10 seconds |
| 5 | 1 in 1,048,576 | ~2 minutes |
| 6 | 1 in 16,777,216 | ~30 minutes |
| 7 | 1 in 268,435,456 | ~8 hours |
| 8+ | 1 in 4,294,967,296+ | Days to weeks |

Times depend on your hardware. Use `--threads` to parallelize.

## Supported Languages for Mnemonics

- English (default)
- Spanish
- French
- Italian
- Japanese
- Korean
- Chinese (Simplified)
- Chinese (Traditional)
- Czech

## How It Works

### Address Generation

1. Generate random 256-bit private key using OS CSPRNG
2. Derive public key using secp256k1 elliptic curve
3. Hash public key with Keccak-256
4. Take last 20 bytes as Ethereum address

### BIP39 Mnemonic

1. Generate random entropy (128-256 bits)
2. Add checksum bits
3. Map to wordlist (2048 words)
4. Derive seed using PBKDF2-HMAC-SHA512
5. Derive keys using BIP32 HD wallet paths

### Message Signing (EIP-191)

1. Prefix message with `\x19Ethereum Signed Message:\n`
2. Hash with Keccak-256
3. Sign with ECDSA secp256k1
4. Return signature (r, s, v)

## Project Structure

```
ethereum-wallet-toolkit/
├── eth_toolkit.py      # Full-featured CLI toolkit (all features)
├── wallet.py           # Standalone wallet generation/restoration
├── keystore.py         # Standalone keystore encryption/decryption
├── sign.py             # Standalone message signing/verification
├── transaction.py      # Standalone offline transaction signing
├── typed_data.py       # Standalone EIP-712 typed data signing
├── validate.py         # Standalone address/key validation
├── vanity.py           # Simple vanity generator (legacy)
├── requirements.txt    # Dependencies
├── README.md           # This file
├── LICENSE             # MIT License
├── docs/               # Documentation
│   ├── API.md          # API reference
│   ├── SECURITY.md     # Security guidelines
│   ├── VANITY.md       # Vanity address guide
│   ├── WALLET.md       # Wallet operations guide
│   ├── KEYSTORE.md     # Keystore operations guide
│   ├── SIGNING.md      # Message signing guide
│   ├── TRANSACTION.md  # Transaction signing guide
│   └── TYPED_DATA.md   # EIP-712 typed data guide
└── tests/              # Test suite
    ├── test_toolkit.py # Main toolkit tests
    └── test_modules.py # Standalone module tests
```

## Comparison with Other Tools

| Feature | This Toolkit | Profanity2 | Vanity-ETH |
|---------|-------------|------------|------------|
| **Library** | eth-account (Official) | Custom OpenCL | secp256k1 |
| **GPU Support** | No | Yes | No (Web Workers) |
| **Mnemonic** | Yes | No | No |
| **HD Wallets** | Yes | No | No |
| **Sign/Verify** | Yes | No | No |
| **Keystore** | Yes | No | No |
| **Transaction Signing** | Yes | No | No |
| **EIP-712 Typed Data** | Yes | No | No |
| **Prefix/Suffix** | Yes | Yes | Yes |
| **Contains** | Yes | Yes | No |
| **Letters/Numbers** | Yes | Yes | No |
| **Mirror** | Yes | Yes | No |
| **Contract Address** | Yes | No | No |
| **Multi-threaded** | Yes | Yes (GPU) | Yes |
| **Auditable** | Yes (~1500 lines) | No (Complex) | Yes |
| **Offline** | Yes | Yes | Yes |

## For AI / LLM / Vibe Coders 🤖

This project includes machine-readable documentation for AI assistants:

- **[llms.txt](llms.txt)** — Quick summary for LLMs
- **[llms-full.txt](llms-full.txt)** — Comprehensive context with code patterns

### Quick Copy-Paste Examples

```python
# Generate wallet with eth-account
from eth_account import Account
account = Account.create()
print(account.address, account.key.hex())

# BIP39 mnemonic wallet
Account.enable_unaudited_hdwallet_features()
account, mnemonic = Account.create_with_mnemonic(num_words=24)

# Sign message (EIP-191)
from eth_account.messages import encode_defunct
signed = Account.sign_message(encode_defunct(text="Hello"), private_key)
```

## Contributing

Contributions welcome. This project aims to be:

- **Official**: Use only Ethereum Foundation libraries
- **Auditable**: Keep code readable and minimal
- **Educational**: Suitable for learning and documentation

## License

MIT License - See [LICENSE](LICENSE) for details.

## Author

**nich** — [@nichxbt](https://x.com/nichxbt) — [github.com/nirholas](https://github.com/nirholas)

## Related Projects

Standalone educational tools (Ethereum Foundation libraries only):

- **[ethereum-address-similarity](https://github.com/nirholas/ethereum-address-similarity)** — Compare addresses for visual similarity
- **[ethereum-gas-estimator](https://github.com/nirholas/ethereum-gas-estimator)** — Calculate gas savings from address zero bytes
- **[ethereum-address-poisoning-detector](https://github.com/nirholas/ethereum-address-poisoning-detector)** — Detect address poisoning attacks

## Related Resources

- [eth-account Documentation](https://github.com/ethereum/eth-account)
- [Web3.py Patterns: Address Mining](https://snakecharmers.ethereum.org/web3-py-patterns-mining-addresses/)
- [BIP39 Specification](https://github.com/bitcoin/bips/blob/master/bip-0039.mediawiki)
- [BIP32 HD Wallets](https://github.com/bitcoin/bips/blob/master/bip-0032.mediawiki)
- [EIP-55 Checksum](https://eips.ethereum.org/EIPS/eip-55)
- [EIP-191 Signed Messages](https://eips.ethereum.org/EIPS/eip-191)
- [EIP-712 Typed Data](https://eips.ethereum.org/EIPS/eip-712)
- [EIP-1559 Transactions](https://eips.ethereum.org/EIPS/eip-1559)
- [Web3 Secret Storage](https://github.com/ethereum/wiki/wiki/Web3-Secret-Storage-Definition)

---
### 🏷️ Keywords

`ethereum` `wallet` `python` `cli` `bip39` `bip32` `hd-wallet` `mnemonic` `vanity-address` `eth-account` `private-key` `address-generator` `message-signing` `eip-191` `secp256k1` `keccak256` `web3` `cryptocurrency` `blockchain` `cold-storage` `offline-wallet` `air-gapped` `open-source` `educational`
---

<p align="center">
  <b>⭐ Star this repo if you find it useful!</b><br>
  <sub>Educational tool for understanding Ethereum wallet mechanics</sub>
</p>


