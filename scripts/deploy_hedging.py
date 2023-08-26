from brownie import accounts, Hedging
from dotenv import load_dotenv

load_dotenv()

def main():
    deployContract(accounts.load('victor'))

def deployContract(_from, _dataFeedAddress):
    deployed = Hedging.deploy(_dataFeedAddress, {
        'from': _from,
        'priority_fee': '10 wei'
    })
    print(f'Contract deployed at: {deployed}')
    return deployed