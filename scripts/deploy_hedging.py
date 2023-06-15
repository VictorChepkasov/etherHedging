from brownie import Hedging, accounts
from dotenv import load_dotenv

load_dotenv()

def deploy_contract(_from):
    hedging_deploy_contract = Hedging.deploy({'from': _from, 'priority_fee': '1 gwei'})
    
    print(f'contract deployed at {hedging_deploy_contract}')

    return hedging_deploy_contract