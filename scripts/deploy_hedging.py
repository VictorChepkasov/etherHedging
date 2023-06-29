from brownie import Hedging, accounts
from dotenv import load_dotenv
from scripts.abi import *

from web3 import Web3, EthereumTesterProvider
w3 = Web3(EthereumTesterProvider())


load_dotenv()

def main():
    a = accounts[0]
    deployContract(a)

def deployContract(_from):
    hedge = w3.eth.contract(address=Hedging[-1].address, abi=EIP20_ABI)
    nonce = w3.eth.get_transaction_count(str(_from))

    tx = hedge.functions.deploy({
        'from': _from,
        'priority_fee': '10 wei'
    }).build_transaction({
        'chainId': 1,
        'gas': 70000,
        'maxFeePerGas': w3.to_wei('2', 'gwei'),
        'maxPriorityFeePerGas': w3.to_wei('1', 'gwei'),
        'nonce': nonce,
    })
    private_key = b"\xb2\\}\xb3\x1f\xee\xd9\x12''\xbf\t9\xdcv\x9a\x96VK-\xe4\xc4rm\x03[6\xec\xf1\xe5\xb3d"
    signed_tx = w3.eth.account.sign_transaction(tx, private_key=private_key)
    print(signed_tx.hash)
    w3.eth.send_raw_transaction(signed_tx.rawTransaction)
    # print(f'contract deployed at {hedgingDeployContract}')
    # return tx