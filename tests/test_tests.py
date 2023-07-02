import pytest
from brownie import accounts
from scripts.deploy_hedging import deployContract
from scripts.scripts import (
    setHedgeInfo,
    getHedgeInfo,
    setContractReactivate,
    pay,
    getLatestETHUSDData,
    getContractBalance
)

@pytest.fixture()
def importAccounts():
    a = accounts.add(private_key="de3ba3f52e698e6f6783741917a058a80b57938ef78322775c14f0798455fac4")
    b = accounts.add(private_key="5248a6634c0f42f814a2055c72731a0b2736b71186a8b9414b354d374358961a")
    return a, b

@pytest.fixture(autouse=True)
def hedge(importAccounts):
    a, b = importAccounts
    contract = deployContract(a)
    return a, b, contract

@pytest.fixture(autouse=True)
def hedgeInfo(hedge):
    setHedgeInfo(hedge[1], 1, hedge[0])
    return hedgeInfo

@pytest.mark.parametrize('deposit', [0, 100])
def test_pay(hedge, hedgeInfo, deposit):
    a, _, _ = hedge
    pay(a, f"{deposit} wei")
    assert getHedgeInfo()[-2] == deposit * getLatestETHUSDData()

@pytest.mark.parametrize('depositA, depositB', [(0, 0), (100, 100), pytest.param((120, 220), 240, marks=pytest.mark.xfail)])
def test_BalanceChanges(hedge, hedgeInfo, depositA, depositB):
    a, b, _ = hedge
    pay(a, f"{depositA} wei")
    pay(b, f"{depositB} wei")
    assert getContractBalance() == 2 * depositA

@pytest.mark.parametrize(
    'shelfLife',
    [0, 7, pytest.param(0.1, marks=pytest.mark.xfail)]
)
def test_HedgeInfo(hedge, shelfLife):
    a, b, _ = hedge
    ethUSDData = (getLatestETHUSDData())
    validHedgeInfo = [False, False, a.address, b.address, ethUSDData, 86400 * shelfLife, 0, 0, 0, False, False, False, False, 0, 0]
    setHedgeInfo(hedge[1], shelfLife, hedge[0])
    assert validHedgeInfo == getHedgeInfo()

def test_contractReactivate(hedge, shelfLife=0):
    a, b, _ = hedge
    setHedgeInfo(b, shelfLife, a)
    #активируем с помощью транзакций (как и задумано)
    pay(a, f"100 wei")
    pay(b, f"100 wei")
    setContractReactivate(a)
    assert getHedgeInfo()[7] > 0
