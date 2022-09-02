from brownie import FundMe, network, config, accounts, MockV3Aggregator
from web3 import Web3

dev_envs = {"development", "ganache-local"}
forked_local_envs = {"mainnet-fork-dev"}


def get_account(dev_envs: set, forked_local_envs):
    # Can define a function here
    if network.show_active() in dev_envs or network.show_active() in forked_local_envs:
        return accounts[0]
    else:
        return accounts.add(config["wallets"]["from_key"])


def deploy_mocks(decimals, starting_price, dev_envs):
    print(f"The network is {network.show_active()}")
    print("Deploying mocks...")
    if len(MockV3Aggregator) <= 0:
        MockV3Aggregator.deploy(
            decimals,
            Web3.toWei(starting_price, "ether"),
            {"from": get_account(dev_envs, forked_local_envs)},
        )
    print("Mocks deployed...")
