
import pytest
from brownie import Hedging, accounts
from scripts.deploy_hedging import deployContract
from scripts.script import setHedgeInfo, getHedgeInfo, payPartyA, payPartyB, getContractBalance 

def test_HedgeInfo():
    a = accounts[0]
    b = accounts[1]
    deployContract(a)

    shelfLife = 1
    validHedgeInfo = (a.address, b.address, 0, 0, 190365,
                        86400 * shelfLife, 0, 0, 0, 
                        False, False, False, False)

    setHedgeInfo(b, shelfLife, a)
    testHedgeInfo = getHedgeInfo()

    assert validHedgeInfo == testHedgeInfo

def test_payA():
    a = accounts[0]
    b = accounts[1]
    contract = deployContract(a)
    deposit = 100
    setHedgeInfo(b, 1, a)
    print(f"Balance A: {getHedgeInfo()[2]}")

    payPartyA(contract, a, f"{deposit} wei")

    assert getHedgeInfo()[2] == deposit * 190365

def test_payB():
    a = accounts[0]
    b = accounts[1]
    contract = deployContract(a)
    deposit = 100
    setHedgeInfo(b, 1, a)
    print(f"Balance B: {getHedgeInfo()[3]}")

    payPartyB(contract, b, f"{deposit} wei")

    assert getHedgeInfo()[3] == deposit * 190365

def test_BalanceChanges():
    a = accounts[0]
    b = accounts[1]
    contract = deployContract(a)
    deposit = 100
    setHedgeInfo(b, 1, a)
    print(f"Balance: {getContractBalance(contract)}")

    payPartyA(contract, a, f"{deposit} wei")
    payPartyB(contract, b, f"{deposit} wei")

    assert getContractBalance(contract) == 2 * deposit
