import os
from web3 import Web3
from web3.contract import Contract
from web3.middleware import geth_poa_middleware
from loguru import logger
from sys import stderr
from dotenv import load_dotenv


def transferTokens(private_key: str,recipient_address: str):
        #Load variables from `.env`
        TOKEN_CONTRACT = os.getenv('TOKEN_CONTRACT')
        CLAIM_CONTRACT = os.getenv('CLAIM_CONTRACT')
        RPC_ARBI = os.getenv('RPC_ARBI')

        # set up Web3 provider
        w3 = Web3(Web3.HTTPProvider(RPC_ARBI))

        # define contract address and ABI
        token_address = TOKEN_CONTRACT
        claim_address = CLAIM_CONTRACT

        address = Web3.to_checksum_address(w3.eth.account.from_key(private_key).address)
        # loads ABIs
        with open('ABI_TOKEN.txt', 'r', encoding='utf-8-sig') as file:
                TOKEN_ABI = file.read().strip().replace('\n', '').replace(' ', '')   
        with open('ABI_CLAIM.txt', 'r', encoding='utf-8-sig') as file:
                CLAIM_ABI = file.read().strip().replace('\n', '').replace(' ', '') 

        # create contracts instances
        contract = w3.eth.contract(address=token_address, abi=TOKEN_ABI)

        claim_address = w3.eth.contract(address=claim_address, abi=CLAIM_ABI)

        claimable_tokens = claim_address.functions.claimableTokens(address).call()

        # set up account to send from
        account = w3.eth.account.from_key(private_key)

        # set up transaction parameters
        recipient = Web3.to_checksum_address(recipient_address)  # address to send tokens to
        amount = claimable_tokens  # amount of tokens to send
        gas_price = w3.to_wei('0.1', 'gwei')
        gas_limit = 600000
        tx = {
        'from': account.address,
        'nonce': w3.eth.get_transaction_count(account.address),
        'gasPrice': gas_price,
        'gas': gas_limit,
        }
        # build transaction
        transaction = contract.functions.transfer(recipient, amount).build_transaction(tx)

        # sign transaction
        signed_txn = w3.eth.account.sign_transaction(transaction, private_key)

        # send transaction
        tx_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)
        print(f'Transaction hash: https://arbiscan.io/tx/{tx_hash.hex()}')
if __name__ == '__main__':
        pass
        print('Successfully load transfer module')