from brownie import Hedging
from dotenv import load_dotenv

load_dotenv()

def deployContract(_from):
    hedgingDeployContract = Hedging.deploy({
        'from': _from,
        'priority_fee': '10 wei'
    })

    print(f'contract deployed at {hedgingDeployContract}')

    return hedgingDeployContract
