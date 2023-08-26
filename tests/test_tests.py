import pytest
from brownie import accounts, network
from scripts.deployHedging import deployContract
from scripts.deployAggregatorV3Testnet import deployAggregatorV3Testnet
from scripts.scripts import (
    getLatestETHUSDData,
    getContractBalance,
    getHedgeInfo,
    setHedgeInfo,
    setContractReactivate,
    pay
)

@pytest.fixture(scope='session')
def importAccounts():
    match network.show_active():
        case 'sepolia': 
            a, b = accounts.load('Party_A'), accounts.load('Party_B')
        case 'development':
            a, b = accounts[0], accounts[1]
    return a, b

@pytest.fixture(autouse=True)
def hedge(importAccounts):
    a, b = importAccounts
    if network.show_active() == 'sepolia':
        _dataFeedAddress = "0x694AA1769357215DE4FAC081bf1f309aDC325306"
    else:
        _dataFeedAddress = deployAggregatorV3Testnet(a)
    contract = deployContract(a, _dataFeedAddress)
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


# Тестирвоание оракула проводится в тестовой сети, поэтому тест идёт последним,
# 0x694AA1769357215DE4FAC081bf1f309aDC325306 - адресс оракула в сети sepolia
# Требования:
#   - Параметр -s для возможности ввода пароля, без него тест провалится
#   - Наличие ETH в сети Sepolia у аккаунта (acc)
def test_getLatestETHUSDData():
    if network.show_active() != 'sepolia':
        network.disconnect()
        network.connect('sepolia')
        print(f"Connected to: {network.show_active()}")
    aсс = accounts.load('Party_B')
    deployContract(aсс, '0x694AA1769357215DE4FAC081bf1f309aDC325306')
    data = getLatestETHUSDData()
    assert data > 0