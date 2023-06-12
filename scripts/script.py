from brownie import Hedging
from scripts import deploy_hedging

# deployed_contract = Hedging[-1]
contract = deploy_hedging.deploy_contract()
value = 0.01

def main():
    print('deployed success!')
    setHedgeInfo('0xa5f78F093C1Fa451eAb7D3102AdF1eC6E0b85F27', 1)
    print('set hedge info!')
    getContractBalance()
    payPartyA(value)
    print('party a sent ether!')
    getContractBalance()
    payPartyB(value)
    print('party b sent ether!')
    getHedgeInfo()
    setContractReactivate()
    getHedgeInfo()


def setHedgeInfo(address, shelfLife):
    contract.setHedgeInfo(address, shelfLife)

def payPartyA(value):
    contract.payPartyA(value)

def payPartyB(value):
    contract.payPartyB(value)

def setContractReactivate():
    contract.setContractReactivate()

def getContractBalance():
    contractBalance = contract.getContractBalance()
    print(f'contract balance: {contractBalance}')

    return contractBalance

def getHedgeInfo():
    hedge = contract.getHedgeInfo()
    print(f'hedge contract info: {hedge}')

    return hedge