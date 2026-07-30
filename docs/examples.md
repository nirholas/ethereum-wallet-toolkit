# ethereum-wallet-toolkit examples

A collection of Ethereum wallet tools: Python CLI utilities (`eth_toolkit.py`, `wallet.py`, `keystore.py`, `sign.py`, `transaction.py`, `typed_data.py`, `validate.py`, `vanity.py`), five Model Context Protocol (MCP) servers exposing wallet functionality to AI assistants, a fully offline single-file HTML wallet (`offlin

## Example 1

```bash
# Navigate to this directory
cd offline-build

# Install dependencies
npm install

# Build offline1.html
npm run build
```

## Example 2

```bash
# Install all servers
pip install -e ./ethereum-wallet-mcp
pip install -e ./keystore-mcp-server
pip install -e ./signing-mcp-server
pip install -e ./transaction-mcp-server
pip install -e ./validation-mcp-server
```

## Example 3

```bash
# Individual servers
pytest ethereum-wallet-mcp/tests/ -v
pytest keystore-mcp-server/tests/ -v
pytest signing-mcp-server/tests/ -v
pytest transaction-mcp-server/tests/ -v
pytest validation-mcp-server/tests/ -v

# All at once
./run_all_tests.sh
```

## Example 4

```text
server-name/
├── pyproject.toml          # Package config
├── README.md               # Server docs
├── src/
│   └── package_name/
│       ├── __init__.py
│       ├── __main__.py     # Entry point
│       ├── server.py       # MCP server setup
│       ├── tools/          # Tool implementations
│       ├── resources/      # Static resources
│       └── prompts/        # Interactive prompts
└── tests/
    └── test_*.py           # Pytest tests
```

## Example 5

```text
Generate a new Ethereum wallet for me
```

## Example 6

```text
Create a new Ethereum wallet with a 24-word seed phrase
```

## Example 7

```text
Generate a test wallet for Sepolia testnet development
```

## Example 8

```text
Restore my wallet from this seed phrase:
abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon about
```


Every snippet above is taken from the [repository documentation](https://github.com/nirholas/ethereum-wallet-toolkit#readme).
