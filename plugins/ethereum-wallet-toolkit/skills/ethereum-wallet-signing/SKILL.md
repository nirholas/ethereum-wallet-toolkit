---
name: ethereum-wallet-signing
description: Generate Ethereum wallets, derive HD accounts, mine vanity addresses and sign or verify EIP-191 and EIP-712 messages offline with the ethereum-wallet-mcp server. Use when an agent needs local key generation or signature checks without a node or RPC.
---

# Ethereum wallet and signing tools

The plugin starts the `ethereum-wallet-mcp` Python server (package on PyPI, Python 3.11 or newer) with `uvx ethereum-wallet-mcp`, over stdio. It needs no env vars, no RPC and no network access. Everything runs locally.

## Security rules first

Several tools take or return a raw private key or mnemonic. Those values pass through the conversation, so treat them as exposed.

- Use generated keys for tests, throwaway wallets and learning. Do not paste a key that holds real funds.
- Never write a returned private key or mnemonic into a file, commit or log unless the user asks.
- Tell the user the secret was shown in the session before they rely on the wallet.

## Wallet tools

- `generate_wallet()` returns `address`, `private_key`, `public_key`.
- `generate_wallet_with_mnemonic(...)` returns a BIP39 wallet with its mnemonic.
- `restore_wallet_from_mnemonic(mnemonic, passphrase="", derivation_path=<default>)`.
- `restore_wallet_from_private_key(private_key)`.
- `derive_multiple_accounts(mnemonic, count=5, start_index=0, passphrase="", base_path=<default>)` for HD batch derivation.
- `generate_vanity_address(prefix="", suffix="", case_sensitive=False, timeout_seconds=60)`. Long patterns take exponentially longer, so keep them short.

## Signing tools (EIP-191 and raw)

- `sign_message(message, private_key)` signs with the personal_sign prefix.
- `sign_message_hex(message_hex, private_key)` signs hex bytes.
- `sign_hash(...)` signs a 32-byte hash directly. Read the tool's parameters from the tool list before calling it, and never sign a hash the user did not produce or approve.
- `verify_message(message, signature, expected_address)` checks a signature against an address.
- `recover_signer(message, signature)` returns the signing address.
- `decompose_signature(signature)` splits into v, r, s. `compose_signature(v, r, s)` joins them.

## EIP-712 typed data tools

- `generate_typed_data_template(...)` produces a starting structure (permit style templates are included).
- `hash_typed_data(typed_data)` returns the digest.
- `sign_typed_data(typed_data, private_key)`.
- `verify_typed_data(...)` and `recover_typed_data_signer(typed_data, signature)`.

## Worked example

1. Call `generate_wallet()` and note the `address`.
2. Call `sign_message` with `message="hello"` and the returned `private_key`.
3. Call `verify_message` with the same message, the signature and the address. It should report a valid match.
4. Call `recover_signer` with the message and signature to confirm it returns the same address.

## Other entry points in the repo

The repo also ships CLI scripts in its root (`wallet.py`, `keystore.py`, `sign.py`, `typed_data.py`, `vanity.py`, `validate.py`, `transaction.py`) and separate MCP packages: `keystore-mcp-server`, `signing-mcp-server`, `transaction-mcp-server`, `validation-mcp-server`. Each has a PyPI console script of the same name. Add one to `.mcp.json` as `uvx <name>` if the user needs keystore, transaction or validation tools, and read its tool list first.
