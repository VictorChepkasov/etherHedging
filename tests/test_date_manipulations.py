import pytest
from brownie import chain
from test_deposit_manipulations import hedge
from scripts.scripts import (
    setHedgeInfo,
    getHedgeInfo,
    pay,
    getLatestETHUSDData,
    setContractReactivate
)

pytestmark = pytest.mark.parametrize(
    'shelfLife',
    [0, 7, 365, pytest.param(0.1, marks=pytest.mark.xfail)]
)
def test_HedgeInfo(hedge, shelfLife=7):
    a, b, _ = hedge
    ethUSDData = getLatestETHUSDData()
    validHedgeInfo = [False, False, a.address, b.address, ethUSDData, 86400 * shelfLife, 0, 0, 0, False, False, False, False, 0, 0]
    setHedgeInfo(hedge[1], shelfLife, hedge[0])
    testHedgeInfo = getHedgeInfo()
    # print(f'VALID: {validHedgeInfo}')
    # print(f'TEST: {testHedgeInfo}')
    assert validHedgeInfo == testHedgeInfo

def test_contractReactivate(hedge, shelfLife):
    a, b, _ = hedge
    setHedgeInfo(b, shelfLife, a)
    #активируем с помощью транзакций (как и задумано)
    pay(a, f"100 wei")
    pay(b, f"100 wei")
    chain.sleep(86400 * shelfLife)
    setContractReactivate(a)
    newHedgeInfo = getHedgeInfo()

    assert newHedgeInfo[7] > 0
