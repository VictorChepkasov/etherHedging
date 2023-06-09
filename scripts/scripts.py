from brownie import Hedging

def setHedgeInfo(_partyB, _shelfLife, _from):
    Hedging[-1].setHedgeInfo(_partyB, _shelfLife, {
        'from': _from,
        'priority_fee': '1 wei'
    })
    print('set hedge info!')

def setContractReactivate(_from):
    Hedging[-1].setContractReactivate({
        'from': _from,
        'priority_fee': '1 wei'
    })

def pay(_a, _deposit):
    print(f'Party {_a} sent ether!')
    Hedging[-1].pay({
        "from": _a,
        "value": _deposit,
        'priority_fee': '1 wei'
    }).wait(1)
    print(f'Party {_a} sent ether!')

def getLatestETHUSDData():
    answer = Hedging[-1].getLatestETHUSDData()
    print(f'ETH/USD latest price: {answer}')
    return answer

def getContractBalance():
    contractBalance = Hedging[-1].getContractBalance()
    print(f'contract balance: {contractBalance}')
    return contractBalance

def getHedgeInfo():
    tmp = Hedging[-1].getHedgeInfo()
    hedge = list(tmp[0])
    for i in tmp[1:]:
        hedge.append(i)
    return list(hedge)