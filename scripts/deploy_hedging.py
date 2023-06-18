from brownie import Hedging
from dotenv import load_dotenv

load_dotenv()

def deployContract(_from):
    hedging_deploy_contract = Hedging.deploy({
        'from': _from,
        'priority_fee': '10 wei'
    })

    print(f'contract deployed at {hedging_deploy_contract}')

    return hedging_deploy_contract