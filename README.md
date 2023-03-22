# ArbitrumMultiClaimerAndSender

# Python implementation multiprocessing of the $ARB token's claimer and sender

## Package description

- `main.py` - main module for execute
- `transfer.py` - module for transfer $ARB-tokens to recipient address

## Description of required files

- `accounts.txt` - private keys of wallets
- `recipient_addresses.txt` - exchange addresses of other addresses for send your claimed tokens
- `.env` - the file with your RPC variables and contract address constants for claim and $ARB-token

_example of `.env`-file_
```sh
TOKEN_CONTRACT = '0xC4ed0A9Ea70d5bCC69f748547650d32cC219D882'
CLAIM_CONTRACT = '0x67a24CE4321aB3aF51c2D0a4801c3E111D88C9d9'
ARBITRUM_MULTI_CALL = '0x842eC2c7D803033Edf55E478F461FC547Bc54EB2'
RPC_ARB = 'https://arb-mainnet.g.alchemy.com/v2/{YOU_API_KEY}'
RPC_MAIN = 'https://eth-mainnet.g.alchemy.com/v2/{YOU_API_KEY}'
```
## How run

- Install Python to your system
- Install dependencies

```sh
pip install -r requierements.txt
```

- Add your private keys to the `accounts.txt` file
- Add your RPCs to the `.env' file
- Add exchange addresses or other addresses for transferring received tokens `recipient_addresses.txt`<br/>
__Count of addresses must correspond to the count of private keys__
- Run `main.py` and wait for `claim` to open

```sh
python .\main.py
```

*for Linux*

```sh
python3 main.py
```
