from brownie import accounts, network
from scripts.deployHedging import deployContract
from scripts.scripts import getLatestETHUSDData
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