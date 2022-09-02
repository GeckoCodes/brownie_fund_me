from brownie import FundMe
from scripts.functions import get_account, deploy_mocks, dev_envs


def fund():
    # Get the contract
    fund_me = FundMe[-1]

    # Get the account to make changes
    account = get_account(dev_envs)

    # Get the entrance fee
    entrance_fee = fund_me.getEntranceFee()
    print(f"The current entry fee is {entrance_fee}")
    print("Funding...")

    # Run the fund
    fund_me.fund({"from": account, "value": entrance_fee})


def withdraw():
    # Get the contract
    fund_me = FundMe[-1]

    # Get the account to make changes
    account = get_account(dev_envs)

    # Do the withdrawal
    fund_me.withdraw({"from": account})


def main():
    fund()
    withdraw()
