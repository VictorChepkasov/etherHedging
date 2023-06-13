from brownie import Hedging, accounts
from dotenv import load_dotenv

load_dotenv()

def deploy_contract(_from):
    hedging_deploy_contract = Hedging.deploy({'from': _from, 'priority_fee': '1 gwei'})
    # hedging_deploy_contract = Hedging.deploy({'from': partyA, 'gas_limit': 100000000000000000000000})

    print(f'contract deployed at {hedging_deploy_contract}')

    return hedging_deploy_contract