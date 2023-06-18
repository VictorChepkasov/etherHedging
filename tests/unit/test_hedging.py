
import pytest
from brownie import accounts
from scripts.deploy_hedging import deployContract
from scripts.script import setHedgeInfo, getHedgeInfo, payPartyA, payPartyB, getContractBalance 

@pytest.fixture(autouse=True)
def hedge():
    a = accounts[0]
    b = accounts[1]
    contract = deployContract(a)

    return a, b, contract

@pytest.fixture(autouse=True)
def hedgeInfo(hedge):
    setHedgeInfo(hedge[1], 1, hedge[0])
    return hedgeInfo

@pytest.mark.parametrize('shelfLife', [0, 7, 365])
def test_HedgeInfo(hedge, shelfLife):
    a, b, _ = hedge
    validHedgeInfo = (a.address, b.address, 0, 0, 190365,
                        86400 * shelfLife, 0, 0, 0, 
                        False, False, False, False)

    setHedgeInfo(b, shelfLife, a)
    testHedgeInfo = getHedgeInfo()

    assert validHedgeInfo == testHedgeInfo

@pytest.mark.parametrize('deposit', [0, 100, 1000000000000])
def test_payA(hedge, hedgeInfo, deposit):
    a, _, contract = hedge
    print(f"Balance A: {getHedgeInfo()[2]}")

    payPartyA(contract, a, f"{deposit} wei")

    assert getHedgeInfo()[2] == deposit * 190365

@pytest.mark.parametrize('deposit', [0, 100, 1000000000000])
def test_payB(hedge, hedgeInfo, deposit):
    _, b, contract = hedge
    print(f"Balance B: {getHedgeInfo()[3]}")

    payPartyB(contract, b, f"{deposit} wei")

    assert getHedgeInfo()[3] == deposit * 190365

@pytest.mark.parametrize('deposit', [0, 100, 1000000000000])
def test_BalanceChanges(hedge, hedgeInfo, deposit):
    a, b, contract = hedge
    print(f"Balance: {getContractBalance(contract)}")

    payPartyA(contract, a, f"{deposit} wei")
    payPartyB(contract, b, f"{deposit} wei")

    assert getContractBalance(contract) == 2 * deposit

