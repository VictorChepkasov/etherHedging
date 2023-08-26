from brownie import accounts, AggregatorV3Testnet

def main():
    deployAggregatorV3Testnet(accounts[0])

def deployAggregatorV3Testnet(_from):
    deployed = AggregatorV3Testnet.deploy({
        'from': _from,
        'priority_fee': '10 wei'
    })
    print(f'AggregatorV3Testnet deployed at {deployed}')
    return deployed