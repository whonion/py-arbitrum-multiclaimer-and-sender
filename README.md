# ArbitrumMultiClaimerAndSender

# Python implementation multiprocessing of the $ARB token's claimer and sender

## Package description

- `main.py` - main module for execute
- `transfer.py` - module for transfer $ARB-tokens to recipient address

## Description of required files

- `accounts.txt` - private keys of wallets
- `recipient_addresses.txt` - Xxchange addresses of other addresses for send your claimed tokens
- `.env` - the file with your RPC variables and contract address constants for claim and $ARB-token

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
