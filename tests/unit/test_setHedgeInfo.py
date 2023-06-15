
import pytest
from brownie import accounts
from scripts.deploy_hedging import deploy_contract
from scripts.script import setHedgeInfo, getHedgeInfo

def test_setHedgeInfo():
    a = accounts[0]
    b = accounts[1]
    deploy_contract(a)
    shelfLife = 1
    validHedgeInfo = (a.address, b.address, 0, 0, 190365,
                        86400 * shelfLife, 0, 0, 0, 
                        False, False, False, False)

    setHedgeInfo(b, shelfLife, a)
    testHedgeInfo = getHedgeInfo()

    assert validHedgeInfo == testHedgeInfo
