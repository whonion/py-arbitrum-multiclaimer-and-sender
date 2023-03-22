import os
import time
from web3 import Web3
from web3.contract import Contract
from web3.middleware import geth_poa_middleware
from loguru import logger
from sys import stderr
from multiprocessing.dummy import Pool
from dotenv import load_dotenv

#from transfer import transferTokens

load_dotenv()
TOKEN_CONTRACT = os.getenv('TOKEN_CONTRACT')
CLAIM_CONTRACT = os.getenv('CLAIM_CONTRACT')
MULTICALL = os.getenv('ARBITRUM_MULTI_CALL')
RPC_ARBI = os.getenv('RPC_ARBI')
#RPC_MAIN = os.getenv('RPC_MAIN')

logger.remove()
logger.add(stderr, format="<white>{time:HH:mm:ss}</white>"
                          " | <level>{level: <8}</level>"
                          " | <cyan>{line}</cyan>"
                          " - <white>{message}</white>")
def getL1blockNumber() -> int:
    #load ABI for Arbitrum multicall contracts
    with open('MULTICALL_ABI.txt', 'r', encoding='utf-8-sig') as file:
            MULTICALL_ABI = file.read().strip().replace('\n', '').replace(' ', '') 
    l1 = Web3(Web3.HTTPProvider(RPC_ARBI))
    l1.middleware_onion.inject(geth_poa_middleware, layer=0)
    multicall = l1.eth.contract(address=Web3.to_checksum_address(MULTICALL),abi=MULTICALL_ABI)
    block_number = multicall.functions.getL1BlockNumber().call()
    return int(block_number)

def calculateGasPrice(private_key,tx:dict):
        w3 = Web3(Web3.HTTPProvider(RPC_ARBI))
        w3.middleware_onion.inject(geth_poa_middleware, layer=0)
        address = Web3.to_checksum_address(w3.eth.account.from_key(private_key).address)
        gas_price = w3.to_wei(str(w3.eth.gas_price), 'wei')
        gas_limit = 600000   
        nonce = w3.eth.get_transaction_count(address)
        tx = {
            'nonce': nonce,
            'gas': gas_limit,
            'gasPrice': gas_price,
        }              
        estimated_gas = w3.eth.estimate_gas(tx)
        gas_limit = int(estimated_gas * 1.3)
        # update the update the gas-parameters of tx
        tx['gas'] = gas_limit
        return tx
def send_tx(args):
    private_key, recipient_address = args
    address = None
    try:
        address = Web3.to_checksum_address(w3.eth.account.from_key(private_key).address)
        gas_price = w3.to_wei(str(w3.eth.gas_price), 'wei')
        gas_limit = 600000   
        nonce = w3.eth.get_transaction_count(address)
        tx_claim = {
            'nonce': nonce,
            'gas': gas_limit,
            'gasPrice': gas_price,
        }      
        #recalculate gas
        tx_claim = calculateGasPrice(private_key=private_key,tx=tx_claim)
        transaction = contract_claim.functions.claim().build_transaction(tx_claim)
        # Sign the transaction with the receiver's private key
        signed_txn = w3.eth.account.sign_transaction(transaction,private_key=private_key)
        
        # Send the transaction to the network
        tx_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)
        # Wait for the transaction to be mined
        receipt = w3.eth.wait_for_transaction_receipt(tx_hash)

        tx_hash = w3.to_hex(w3.keccak(signed_txn.rawTransaction))
        # Check if the transaction was successful
        if receipt['status'] == 1:
            # Get the amount of tokens claimed
            claimable_tokens = contract_claim.functions.claimableTokens(address).call()
            ARB = claimable_tokens/1000000000000000000
            print(f'{ARB} $ARB tokens were successfully claimed to {address}.')
            logger.info(f'{address} | https://arbiscan.io/tx/{tx_hash}')
            # Set up the transaction parameters for sending tokens
            token_amount = claimable_tokens
            if claimable_tokens > 0:
                    token_amount = int(claimable_tokens)            
            nonce = w3.eth.get_transaction_count(address)
            gas_price = w3.to_wei(str(w3.eth.gas_price), 'wei')
            tx_send = {
                'nonce': nonce,
                'gasPrice': gas_price,
                'gas': gas_limit
            }              
            tx_send = calculateGasPrice(private_key=private_key,tx=tx_send)
            recipient_address = w3.to_checksum_address(recipient_address)  # Convert recipient address to Ethereum address object
            token_transaction = contract_token.functions.transfer(recipient_address, token_amount).build_transaction(tx_send)        
        else:
            raise ValueError(f"Claim transaction failed with receipt status {receipt['status']}")
        
        if token_transaction:
            signed_txn = w3.eth.account.sign_transaction(token_transaction, private_key=private_key)
            tx_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)
            logger.info(f'Sending tokens from {address} to {recipient_address} | https://arbiscan.io/tx/{tx_hash.hex()}')

            # Wait for the transaction to be mined
            tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
            logger.info(f'Tokens sent from {address} to {recipient_address} | Transaction confirmed in block {tx_receipt.blockNumber}')
        else:
            raise ValueError("Token transaction was not initialized")
    except Exception as error:
        logger.error(f'{address} | {error}')

if __name__ == '__main__':
    print('-' * 108)
    print((' '*32)+'ARBITRUM MULTI SENDER AND CLAIMER'+(' '*32))
    print('-' * 108)
    with open('accounts.txt', encoding='utf-8-sig') as file:
        private_keys = [row.strip() for row in file]

    w3 = Web3(Web3.HTTPProvider(RPC_ARBI))
    w3.middleware_onion.inject(geth_poa_middleware, layer=0)
    
    with open('recipient_addresses.txt', 'r', encoding='utf-8-sig') as file:
            recipient_addresses = file.read().strip().replace('\n', '').replace(' ', '')  
    #load ABI for contracts
    with open('ABI_CLAIM.txt', 'r', encoding='utf-8-sig') as file:
            CLAIM_ABI = file.read().strip().replace('\n', '').replace(' ', '') 
    with open('ABI_TOKEN.txt', 'r', encoding='utf-8-sig') as file:
            TOKEN_ABI = file.read().strip().replace('\n', '').replace(' ', '')   
    contract_claim = w3.eth.contract(address=Web3.to_checksum_address(CLAIM_CONTRACT),
                               abi=CLAIM_ABI)
    contract_token = w3.eth.contract(address=Web3.to_checksum_address(TOKEN_CONTRACT),
                               abi=TOKEN_ABI)    
    logger.info(f'Loads {len(private_keys)} wallets')

    #mainnet = Web3(Web3.HTTPProvider(RPC_MAIN))
    target_block = 16890400 #claimPeriodStart
    timestamp = 16875614 #timestamp
    # function claim() public {
    # require(block.number >= claimPeriodStart, "TokenDistributor: claim not started");
    # require(block.number < claimPeriodEnd, "TokenDistributor: claim ended");

    # uint256 amount = claimableTokens[msg.sender];
    # require(amount > 0, "TokenDistributor: nothing to claim");

    # claimableTokens[msg.sender] = 0;

    # // we don't use safeTransfer since impl is assumed to be OZ
    # require(token.transfer(msg.sender, amount), "TokenDistributor: fail token transfer");
    # emit HasClaimed(msg.sender, amount);
    # }
    while True:
        #Get the current block number
        current_block = getL1blockNumber()
        current_timestamp = int(time.time())
        print(f'Currect Ethereum block: {current_block} The transaction will be sent after the block: {target_block}')
        # #Check if the target block has been reached
        if current_block >= target_block and current_timestamp >= timestamp:
            with Pool(processes=len(private_keys)) as executor:
                args = zip(private_keys, [recipient_addresses] * len(private_keys))
                executor.map(send_tx, args)
            input('Press Enter To Exit..')