import json
from algosdk.mnemonic import *
from algosdk.future import transaction
from algosdk.atomic_transaction_composer import *
from algosdk.logic import get_application_address
from utils.constants import ALGOD_HOST, ALGOD_TOKEN, APP_ACCOUNT_MNEMONIC
from beaker import *
from contracts.emission_control import EmissionControl

ACCOUNT_ADDRESS = to_public_key(APP_ACCOUNT_MNEMONIC)
ACCOUNT_SECRET = to_private_key(APP_ACCOUNT_MNEMONIC)
ACCOUNT_SIGNER = AccountTransactionSigner(ACCOUNT_SECRET)

WAIT_DELAY = 11


class EmissionControlClient:
    """
    EmissionControl client interfacing with the Emission Control SC deployed on the algorand blockchain
    """

    def __init__(self, app_id: int = 0):
        self._algo_client = None
        self._algo_app = None
        self._app_id = app_id
        self._app_address = None

        self.build_client(app_id)

    def get_app_id(self):
        return self._app_id

    def get_app_address(self):
        return self._app_address

    def build_algo_client(self):
        algod_client = algod.AlgodClient(ALGOD_TOKEN, ALGOD_HOST)
        return algod_client

    def get_algo_app_client(self, app_id: int):
        app_client = client.ApplicationClient(
            self._algo_client,
            ComplianceContract(),
            signer=ACCOUNT_SIGNER,
            app_id=self._app_id,
        )
        if app_id == 0:
            # Create  an app client for our app
            app_id, app_addr, _ = app_client.create()
            print(f"Created Compliance app at {app_id} {app_addr}")
            self._app_id = app_id
            app_client.fund(1 * consts.algo)
            print("Funded app")
            app_client.opt_in()
            print("Opted in")
        else:
            app_addr = get_application_address(app_id)
        self._app_address = app_addr
        return app_client

    def build_client(self, app_id: int):
        self._algo_client = self.build_algo_client()
        self._algo_app = self.get_algo_app_client(app_id)
        assert all(
            [
                self._algo_client,
                self._algo_app,
                self._app_id,
                self._app_address,
            ]
        )

    def get_application_state(self):
        app_state = self._algo_client.dele
        print(f"Current app state:{app_state}")
        return app_state

    def get_application_state(self):
        app_state = self._algo_app.get_application_state()
        print(f"Current app state:{app_state}")
        return app_state

    def get_application_address(self):
        app_addr = get_application_address(self._app_id)
        print(f"Current app address:{app_addr}")
        return app_addr

    def get_emissions_rule(self):
        sp = self._algo_client.suggested_params()
        sp.flat_fee = True
        sp.fee = 2000  # cover this and 1 inner transaction

        res = self._algo_app.call(
            ComplianceContract.get_emission_rule,
            suggested_params=sp,
        )
        print("======== res is: ", res)
        print("======== res.return_value is: ", res.return_value)
        print("======== res.raw_value is: ", res.raw_value)
        print("======== res.tx_id is: ", res.tx_id)
        print("======== res.tx_value is: ", res.tx_info)
        return res

    def set_emissions_rule(self, emission_param: str, emission_max: int):
        sp = self._algo_client.suggested_params()
        sp.flat_fee = True
        sp.fee = 2000  # cover this and 1 inner transaction

        res = self._algo_app.call(
            ComplianceContract.set_emission_rule,
            emission_parameter=emission_param,
            emission_max=emission_max,
            emission_min=0,
            suggested_params=sp,
        )
        print("======== res is: ", res)
        print("======== res.return_value is: ", res.return_value)
        print("======== res.raw_value is: ", res.raw_value)
        print("======== res.tx_id is: ", res.tx_id)
        print("======== res.tx_value is: ", res.tx_info)
        return res

    def is_business_compliant(self, emission_param: str, emission_val: str):
        sp = self._algo_client.suggested_params()
        sp.flat_fee = True
        sp.fee = 2000  # cover this and 1 inner transaction

        res = self._algo_app.call(
            ComplianceContract.is_business_compliant,
            emission_parameter=emission_param,
            emission_value=int(emission_val),
            suggested_params=sp,
        )
        print("======== res is: ", res)
        print("======== res.return_value is: ", res.return_value)
        print("======== res.raw_value is: ", res.raw_value)
        print("======== res.tx_id is: ", res.tx_id)
        print("======== res.tx_value is: ", res.tx_info)
        return res

    def create_compliance_token(self, business_address: str):
        """
        This functions mints the compliance NFT with the business address as the owner of the NFT,
        for being in compliance with the emission control set by the regulator
        """
        sp = self._algo_client.suggested_params()
        sp.flat_fee = True
        sp.fee = 5000  # cover this and 1 inner transaction

        res = self._algo_app.call(
            ComplianceContract.create_compliance_nft,
            business_address=business_address,
            suggested_params=sp,
            accounts=[business_address],
        )
        print("======== res is: ", res)
        print("======== res.return_value is: ", res.return_value)
        print("======== res.raw_value is: ", res.raw_value)
        print("======== res.tx_id is: ", res.tx_id)
        print("======== res.tx_value is: ", res.tx_info)
        return res

    def transfer_compliance_token_to_business(
        self, business_address: str, asset_id: int
    ):
        """
        This functions mints the compliance NFT with the business address as the owner of the NFT,
        for being in compliance with the emission control set by the regulator
        """
        sp = self._algo_client.suggested_params()
        sp.flat_fee = True
        sp.fee = 5000  # cover this and 1 inner transaction

        res = self._algo_app.call(
            ComplianceContract.allocate_compliance_nft_to_business,
            business_address=business_address,
            asset_id=asset_id,
            suggested_params=sp,
            accounts=[business_address],
            foreign_assets=[asset_id],
        )
        print("======== res is: ", res)
        print("======== res.return_value is: ", res.return_value)
        print("======== res.raw_value is: ", res.raw_value)
        print("======== res.tx_id is: ", res.tx_id)
        print("======== res.tx_value is: ", res.tx_info)
        return res

    def create_reward_tokens_supply(self):
        sp = self._algo_client.suggested_params()
        sp.flat_fee = True
        sp.fee = 5000  # cover this and 1 inner transaction

        res = self._algo_app.call(
            ComplianceContract.create_reward_token_supply,
            suggested_params=sp,
        )
        print("======== res is: ", res)
        print("======== res.return_value is: ", res.return_value)
        print("======== res.raw_value is: ", res.raw_value)
        print("======== res.tx_id is: ", res.tx_id)
        print("======== res.tx_value is: ", res.tx_info)
        return res

    def transfer_reward_token_to_business(
        self, business_address: str, asset_id: int
    ):
        """
        This functions mints the compliance NFT with the business address as the owner of the NFT,
        for being in compliance with the emission control set by the regulator
        """
        sp = self._algo_client.suggested_params()
        sp.flat_fee = True
        sp.fee = 5000  # cover this and 1 inner transaction

        res = self._algo_app.call(
            ComplianceContract.allocate_reward_token_to_business,
            business_address=business_address,
            asset_id=asset_id,
            suggested_params=sp,
            accounts=[business_address],
            foreign_assets=[asset_id],
        )
        print("======== res is: ", res)
        print("======== res.return_value is: ", res.return_value)
        print("======== res.raw_value is: ", res.raw_value)
        print("======== res.tx_id is: ", res.tx_id)
        print("======== res.tx_value is: ", res.tx_info)
        return res

    #   Utility function used to print asset holding for account and assetid
    def print_asset_holding(self, account, asset_id):
        # note: if you have an indexer instance available it is easier to just use this
        # response = myindexer.accounts(asset_id = assetid)
        # then loop thru the accounts returned and match the account you are looking for
        account_info = self._algo_client.account_info(account)
        idx = 0
        # print("========= account info: ", account_info)
        for my_account_info in account_info["assets"]:
            scrutinized_asset = account_info["assets"][idx]
            idx = idx + 1
            # print("========= asset info: ", account_info['assets'])
            print(
                "========= created asset info: ",
                account_info["created-assets"],
            )
            if scrutinized_asset["asset-id"] == asset_id:
                # print(json.dumps(scrutinized_asset))
                # print("Asset ID: {}".format(scrutinized_asset['asset-id']))
                # print(json.dumps(scrutinized_asset, indent=4))
                break


if __name__ == "__main__":
    print("Starting deploy of the Compliance App(SC) on Algorand...")
    # appId:120027745
    c = ComplianceClient(120076235)
    c.get_application_state()
    c.get_application_address()
    c.get_emissions_rule()
    print("================ CHANGE =====================")
    # c.set_emissions_rule()
    # print("================ CHANGE =====================")
    # c.get_emissions_rule()
    # print("================ CHANGE =====================")
    # try:
    #     c.is_business_compliant()
    # except Exception as e:
    #     print("============ EXCEPTION: ", e)
    #
    # try:
    #     c.create_compliance_token("SZ3K22H6MZ3A3ORYIVTAYMQMMBWVFOMJWXR3QCODNMJBQRIKBXN5PXX6AI")
    # except Exception as e:
    #     print("========= EXCEPTION IN CREATING COMPLIANCE NFT...", e)
    #     import traceback
    #     traceback.print_exc()

    # try:
    #     c.transfer_compliance_token_to_business("SZ3K22H6MZ3A3ORYIVTAYMQMMBWVFOMJWXR3QCODNMJBQRIKBXN5PXX6AI", 120023374)
    # except Exception as e:
    #     print("========= EXCEPTION IN TRANSFERRING TO BUSINESS...", e)
    #     import traceback
    #     traceback.print_exc()

    # try:
    #     c.print_asset_holding("SZ3K22H6MZ3A3ORYIVTAYMQMMBWVFOMJWXR3QCODNMJBQRIKBXN5PXX6AI", 120019312)
    # except Exception as e:
    #     print("========= EXCEPTION IN GETTING ACCOUNT INFO...", e)
    #     import traceback
    #     traceback.print_exc()

    # """
    # Reward Token interactions below!
    # """
    # # c.create_reward_tokens_supply()
    # try:
    #     c.transfer_reward_token_to_business(
    #         "C25IIJNW7VRRPNPEBKNBU2TR4SGIIH22EGYGE6FWXLGOV4GDQMN5VGTWB4",
    #         120027897,
    #     )
    # except Exception as e:
    #     print("========= EXCEPTION IN TRANSFERRING TO BUSINESS...", e)
    #     import traceback
    #
    #     traceback.print_exc()
