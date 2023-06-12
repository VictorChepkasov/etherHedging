from brownie import Hedging, accounts
from dotenv import load_dotenv

load_dotenv()

partyA = accounts.load('victor')

def main():
    deploy_contract()
    print('deployed success!')

def deploy_contract():
    hedging_deploy_contract = Hedging.deploy({'from': partyA, 
                                              'priority_fee': '1 wei'})
    # hedging_deploy_contract = Hedging.deploy({'from': partyA, 'gasPrice': 100000000000000000})

    print(f'contract deployed at {hedging_deploy_contract}')

    return hedging_deploy_contract