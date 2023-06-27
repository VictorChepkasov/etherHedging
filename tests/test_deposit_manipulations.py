
import pytest
from brownie import accounts, network
from scripts.deploy_hedging import deployContract
from scripts.scripts import (
    setHedgeInfo,
    getHedgeInfo,
    pay,
    getLatestETHUSDData,
    getContractBalance
)

@pytest.fixture(autouse=True)
def hedge():
    a = accounts.load('victor')
    b = accounts.load('victor2')
    contract = deployContract(a)
    return a, b, contract

@pytest.fixture(autouse=True)
def hedgeInfo(hedge):
    setHedgeInfo(hedge[1], 1, hedge[0])
    return hedgeInfo

@pytest.mark.parametrize('deposit', [0, 100, 1000000000000])
def test_pay(hedge, hedgeInfo, deposit):
    a, _, _ = hedge
    print(f"Balance : {getHedgeInfo()[-2]}")
    pay(a, f"{deposit} wei")
    assert getHedgeInfo()[-2] == deposit * getLatestETHUSDData(a)

@pytest.mark.parametrize('depositA, depositB', [(0, 0), (100, 100), (1000000000000, 1000000000000), pytest.param((120, 220), 240, marks=pytest.mark.xfail)])
def test_BalanceChanges(hedge, hedgeInfo, depositA, depositB):
    a, b, _ = hedge
    print(f"Balance: {getContractBalance()}")
    pay(a, f"{depositA} wei")
    pay(b, f"{depositB} wei")
    assert getContractBalance() == 2 * depositA