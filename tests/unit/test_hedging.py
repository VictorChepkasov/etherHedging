
import pytest
from brownie import accounts, chain
from scripts.deploy_hedging import deployContract
from scripts.scripts import (
    setHedgeInfo,
    getHedgeInfo,
    pay,
    getContractBalance,
    setContractReactivate
)

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

@pytest.mark.parametrize(
    'shelfLife',
    [0, 7, 365, pytest.param(0.1, marks=pytest.mark.xfail)]
)
def test_HedgeInfo(hedge, shelfLife):
    a, b, _ = hedge
    validHedgeInfo = [False, False, a.address, b.address, 190365, 86400 * shelfLife, 0, 0, 0, False, False, False, False, 0, 0]
    setHedgeInfo(hedge[1], shelfLife, hedge[0])
    testHedgeInfo = getHedgeInfo()
    assert validHedgeInfo == testHedgeInfo

@pytest.mark.parametrize('deposit', [0, 100, 1000000000000])
def test_pay(hedge, hedgeInfo, deposit):
    a, _, _ = hedge
    print(f"Balance : {getHedgeInfo()[-2]}")
    pay(a, f"{deposit} wei")
    assert getHedgeInfo()[-2] == deposit * 190365

@pytest.mark.parametrize('depositA, depositB', [(0, 0), (100, 100), (1000000000000, 1000000000000), pytest.param((120, 220), 240, marks=pytest.mark.xfail)])
def test_BalanceChanges(hedge, hedgeInfo, depositA, depositB):
    a, b, _ = hedge
    print(f"Balance: {getContractBalance()}")
    pay(a, f"{depositA} wei")
    pay(b, f"{depositB} wei")
    assert getContractBalance() == 2 * depositA

@pytest.mark.parametrize(
    'shelfLife',
    [0, 7, 365, pytest.param(0.1, marks=pytest.mark.xfail)]
)
def test_contractReactivate(hedge, shelfLife):
    a, b, contract = hedge
    setHedgeInfo(b, shelfLife, a)
    #активируем с помощью транзакций (как и задумано)
    pay(a, f"100 wei")
    pay(b, f"100 wei")
    chain.sleep(86400 * shelfLife)
    setContractReactivate(a)
    newHedgeInfo = getHedgeInfo()

    assert newHedgeInfo[7] > 0