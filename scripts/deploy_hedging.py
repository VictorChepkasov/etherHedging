from brownie import Hedging, accounts
from dotenv import load_dotenv

load_dotenv()

# def main():
#     a = accounts[0]
#     deployContract(a)

def deployContract(_from):
    hedgingDeployContract = Hedging.deploy({
        'from': _from,
        'priority_fee': '10 wei'
    })
    print(f'contract deployed at {hedgingDeployContract}')
    return hedgingDeployContract