import pytest
from brownie import chain, network, accounts
from tests.test_tests import hedge
from scripts.deploy_hedging import deployContract
from scripts.scripts import (
    setHedgeInfo,
    getHedgeInfo,
    pay,
    getLatestETHUSDData,
    setContractReactivate
)

@pytest.mark.parametrize(
    'shelfLife',
    [0, 7, pytest.param(0.1, marks=pytest.mark.xfail)]
)
def test_HedgeInfo(hedge, shelfLife):
    a, b, _ = hedge
    ethUSDData = (getLatestETHUSDData())
    validHedgeInfo = [False, False, a.address, b.address, ethUSDData, 86400 * shelfLife, 0, 0, 0, False, False, False, False, 0, 0]
    setHedgeInfo(hedge[1], shelfLife, hedge[0])
    testHedgeInfo = getHedgeInfo()
    assert validHedgeInfo == testHedgeInfo

def test_contractReactivate(hedge, shelfLife=0):
    a, b, _ = hedge
    setHedgeInfo(b, shelfLife, a)
    #активируем с помощью транзакций (как и задумано)
    pay(a, f"100 wei")
    pay(b, f"100 wei")
    setContractReactivate(a)
    newHedgeInfo = getHedgeInfo()
    assert newHedgeInfo[7] > 0
