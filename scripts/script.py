from brownie import Hedging, accounts
from scripts import deploy_hedging

def setHedgeInfo(_address, _shelfLife, _from):
    Hedging[-1].setHedgeInfo(_address, _shelfLife, {'from': _from, 'priority_fee': '1 wei'})
    print('set hedge info!')

def setContractReactivate(contract, _from):
    contract.setContractReactivate({'from': _from, 'priority_fee': '1 wei'})

def payPartyA(contract, _a, _deposit):
    print('Party A sending Ether')
    contract.payPartyA({"from": _a, "value": _deposit, 'priority_fee': '1 wei'})
    print('party A sent ether!')
    # getHedgeInfo()

def payPartyB(contract, _b, _deposit):
    print('Party B sending Ether')
    contract.payPartyB({"from": _b, "value": _deposit, 'priority_fee': '1 wei'})
    print('party B sent ether!')
    # getHedgeInfo()

def getContractBalance(contract):
    contractBalance = contract.getContractBalance()
    print(f'contract balance: {contractBalance}')

    return contractBalance

def getHedgeInfo():
    hedge = Hedging[-1].getHedgeInfo()
    # print(f'''hedge contract info: 
    #       A: {hedge[0]}
    #       B: {hedge[1]}
    #       A balance: {hedge[2]}
    #       B balance: {hedge[3]}
    #       ETH/USD price: {hedge[4]}
    #       Shelf Life: {hedge[5]}
    #       Date of create: {hedge[6]}
    #       Date of reactivate: {hedge[7]}
    #       Date of close: {hedge[8]}
    #       A input Eth: {hedge[9]}
    #       B input Eth: {hedge[10]}
    #       A received Eth: {hedge[11]} 
    #       B received Eth: {hedge[12]}''')

    return hedge 