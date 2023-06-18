
import pytest
from brownie import Hedging, accounts
from scripts.deploy_hedging import deployContract
from scripts.script import setHedgeInfo, getHedgeInfo, payPartyA, payPartyB, getContractBalance 

@pytest.fixture
def hedge():
    a = accounts[0]
    b = accounts[1]
    contract = deployContract(a)

    return a, b, contract

@pytest.fixture
def hedgeInfo(hedge):
    setHedgeInfo(hedge[1], 1, hedge[0])
    return hedgeInfo

def test_HedgeInfo(hedge):
    a, b, _ = hedge
    shelfLife = 1
    validHedgeInfo = (a.address, b.address, 0, 0, 190365,
                        86400 * shelfLife, 0, 0, 0, 
                        False, False, False, False)

    setHedgeInfo(b, shelfLife, a)
    testHedgeInfo = getHedgeInfo()

    assert validHedgeInfo == testHedgeInfo

def test_payA(hedge, hedgeInfo):
    a, _, contract = hedge
    deposit = 100
    print(f"Balance A: {getHedgeInfo()[2]}")

    payPartyA(contract, a, f"{deposit} wei")

    assert getHedgeInfo()[2] == deposit * 190365

def test_payB(hedge, hedgeInfo):
    _, b, contract = hedge
    deposit = 100
    print(f"Balance B: {getHedgeInfo()[3]}")

    payPartyB(contract, b, f"{deposit} wei")

    assert getHedgeInfo()[3] == deposit * 190365

def test_BalanceChanges(hedge, hedgeInfo):
    a, b, contract = hedge
    deposit = 100
    print(f"Balance: {getContractBalance(contract)}")

    payPartyA(contract, a, f"{deposit} wei")
    payPartyB(contract, b, f"{deposit} wei")

    assert getContractBalance(contract) == 2 * deposit
