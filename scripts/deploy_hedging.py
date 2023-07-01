from brownie import Hedging, accounts
from dotenv import load_dotenv

load_dotenv()

# def main():
#     a = accounts.add(private_key="de3ba3f52e698e6f6783741917a058a80b57938ef78322775c14f0798455fac4")
#     # b = accounts.add(private_key="5248a6634c0f42f814a2055c72731a0b2736b71186a8b9414b354d374358961a")
#     deployContract(a)

def deployContract(_from):
    deployed = Hedging.deploy({
        'from': _from,
        'priority_fee': '10 wei'
    })
    print(f'Contract deployed at: {deployed}')
    return deployed