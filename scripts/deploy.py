# As before we can just import the contract
from brownie import FundMe, network, config, accounts, MockV3Aggregator
from scripts.functions import get_account, deploy_mocks, dev_envs, forked_local_envs
from web3 import Web3


def deploy_fund_me():

    account = get_account(dev_envs, forked_local_envs)

    # If we add the API key for etherscan to the environment variables, then we can publish the source code

    # Going to pass the price feed address to the fundme contract - just add the variable in!

    # If we are on the persistent network use the associated address otherwise deploy mocks
    # In the brownie config can add different

    if network.show_active() not in dev_envs:
        price_feed_address = config["networks"][network.show_active()][
            "eth_usd_price_feed"
        ]
    else:
        # If we are on development then we can mock this - create a test folder in the contracts
        # Can pull from the chainlink mix repo
        deploy_mocks(decimals=18, starting_price=2000, dev_envs=dev_envs)
        price_feed_address = MockV3Aggregator[-1].address

    fund_me = FundMe.deploy(
        price_feed_address,
        {"from": account},
        publish_source=config["networks"][network.show_active()].get("verify"),
    )

    print(f"Contract deployed to {fund_me.address}")
    return fund_me


def main():
    deploy_fund_me()
