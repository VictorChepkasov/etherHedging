from brownie import Hedging, accounts
from scripts import deploy_hedging

a = accounts.load('victor')
b = accounts.load('victor2')
value = 1
deposit = "10000 wei"

contract = deploy_hedging.deploy_contract(a)
# print('deployed success!')

def main():
    setHedgeInfo(b, 1)
    getHedgeInfo()
    getContractBalance()
    payPartyA()
    getContractBalance()
    payPartyB()
    getContractBalance() 
    
    # setContractReactivate()
    # getHedgeInfo()


def setHedgeInfo(address, shelfLife):
    contract.setHedgeInfo(address, shelfLife, {'from': a})
    print('set hedge info!')

def payPartyA():
    print('Party A sending Ether')
    contract.payPartyA({"from": a, "value": deposit})
    print('party a sent ether!')
    getHedgeInfo()

def payPartyB():
    print('Party B sending Ether')
    contract.payPartyB({"from": b, "value": deposit})
    print('party b sent ether!')
    getHedgeInfo()

def setContractReactivate():
    contract.setContractReactivate({'from': a})

def getContractBalance():
    contractBalance = contract.getContractBalance()
    print(f'contract balance: {contractBalance}')

    return contractBalance

def getHedgeInfo():
    hedge = contract.getHedgeInfo()
    print(f'''hedge contract info: 
          A: {hedge[0]}
          B: {hedge[1]}
          A ballance: {hedge[2]}
          B balance: {hedge[3]}
          ETH/USD price: {hedge[4]}
          Shelf Life: {hedge[5]}
          Date of create: {hedge[6]}
          Date of reactivate: {hedge[7]}
          Date of close: {hedge[8]}
          A input Eth: {hedge[9]}
          B input Eth: {hedge[10]}
          A received Eth: {hedge[11]} 
          B received Eth: {hedge[12]}''')

    return hedge 