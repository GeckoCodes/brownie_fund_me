from scripts.functions import get_account, deploy_mocks, dev_envs, forked_local_envs
from scripts.deploy import deploy_fund_me
from brownie import FundMe, network, config, accounts, MockV3Aggregator
import pytest
from pytest import raises
from brownie.exceptions import VirtualMachineError


def test_can_fund_withdraw():
    # Get account
    account = get_account(dev_envs, forked_local_envs)

    # Fund me function
    fund_me = deploy_fund_me()

    # Get the entrance fee
    entrance_fee = fund_me.getEntranceFee() + 100

    # Make the fund transaction
    tx = fund_me.fund({"from": account, "value": entrance_fee})
    tx.wait(1)

    # Run assertions
    assert fund_me.addressToAmountFunded(account.address) == entrance_fee

    # Withdraw
    tx2 = fund_me.withdraw({"from": account})
    assert fund_me.addressToAmountFunded(account.address) == 0


# Don't always want to test all of our functionality on live networks as it will take a long time
def test_only_owner_can_withdraw():
    if network.show_active() not in dev_envs:
        pytest.skip("only for local testing")

    # Load the contract
    fund_me = deploy_fund_me()

    # Try to withdraw from a different account
    bad_actor = accounts.add()

    with pytest.raises(VirtualMachineError):
        fund_me.withdraw({"from": bad_actor})
