from brownie import Hedging
from dotenv import load_dotenv

load_dotenv()

def deployContract(_from):
    deployed = Hedging.deploy({
        'from': _from,
        'priority_fee': '10 wei'
    })
    print(f'Contract deployed at: {deployed}')
    return deployed