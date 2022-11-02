import json
import os
from algosdk.mnemonic import *
from algosdk.future import transaction
from algosdk.future.transaction import *
from algosdk.future.transaction import (
    AssetConfigTxn,
    AssetTransferTxn,
    AssetFreezeTxn,
)
from algosdk.atomic_transaction_composer import *
from algosdk.logic import get_application_address
from utils.constants import (
    ALGOD_HOST,
    ALGOD_TOKEN,
    APP_ACCOUNT_MNEMONIC,
    EMISSION_CONTROL_FILE,
    EMISSION_CONTROL_ASSET_FILE,
    BUSINESS1_ACCOUNT_MNEMONIC,
)
from beaker import *
from contracts.emission_control import EmissionControl
from pathlib import Path

ACCOUNT_ADDRESS = to_public_key(APP_ACCOUNT_MNEMONIC)
ACCOUNT_SECRET = to_private_key(APP_ACCOUNT_MNEMONIC)
ACCOUNT_SIGNER = AccountTransactionSigner(ACCOUNT_SECRET)

BUSINESS1_ACCOUNT_ADDRESS = to_public_key(BUSINESS1_ACCOUNT_MNEMONIC)
BUSINESS1_ACCOUNT_SECRET = to_private_key(BUSINESS1_ACCOUNT_MNEMONIC)
BUSINESS1_ACCOUNT_SIGNER = AccountTransactionSigner(BUSINESS1_ACCOUNT_SECRET)

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

    def print_txn(self, txn):
        print("=============== BLOCKCHAIN INTERACTION RESULT ===============")
        print(
            f"TXN: {txn.tx_id}, RESULT: {txn.raw_value}, RETURN_VAL: {txn.return_value}"
        )
        print("=============== BLOCKCHAIN INTERACTION RESULT ===============")

    def get_algo_app_client(self, app_id: int):
        app_client = client.ApplicationClient(
            self._algo_client,
            EmissionControl(),
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
            EmissionControl.get_emission_rule,
            suggested_params=sp,
        )
        self.print_txn(res)
        return res

    def set_emissions_rule(self, emission_param: str, emission_max: int):
        sp = self._algo_client.suggested_params()
        sp.flat_fee = True
        sp.fee = 2000  # cover this and 1 inner transaction

        res = self._algo_app.call(
            EmissionControl.set_emission_rule,
            emission_parameter=emission_param,
            emission_max=emission_max,
            emission_min=0,
            suggested_params=sp,
        )
        self.print_txn(res)
        return res

    def is_business_compliant(self, emission_param: str, emission_val: int):
        sp = self._algo_client.suggested_params()
        sp.flat_fee = True
        sp.fee = 2000  # cover this and 1 inner transaction

        res = self._algo_app.call(
            EmissionControl.is_business_compliant,
            emission_parameter=emission_param,
            emission_value=emission_val,
            suggested_params=sp,
        )
        self.print_txn(res)
        return res

    def create_compliance_token(self):
        """
        This functions mints the compliance NFT with the business address as the owner of the NFT,
        for being in compliance with the emission control set by the regulator
        """
        sp = self._algo_client.suggested_params()
        sp.flat_fee = True
        sp.fee = 5000  # cover this and 1 inner transaction

        res = self._algo_app.call(
            EmissionControl.create_compliance_nft,
            suggested_params=sp,
        )
        self.print_txn(res)
        return res

    def opt_into_compliance_nft(self, business_address: str, asset_id: int):
        """
        This function calls the opt_in method of the app to opt the business into the token!
        :param asset_id:
        :return:
        """
        sp = self._algo_client.suggested_params()
        sp.flat_fee = True
        sp.fee = 5000  # cover this and 1 inner transaction

        txn = AssetTransferTxn(
            sender=business_address,
            sp=sp,
            receiver=business_address,
            amt=0,
            index=asset_id,
        )
        stxn = txn.sign(BUSINESS1_ACCOUNT_SECRET)
        # Send the transaction to the network and retrieve the txid.
        try:
            txid = self._algo_client.send_transaction(stxn)
            print("Signed transaction with txID: {}".format(txid))
            # Wait for the transaction to be confirmed
            confirmed_txn = wait_for_confirmation(self._algo_client, txid, 4)
            print("TXID: ", txid)
            print(
                "Result confirmed in round: {}".format(
                    confirmed_txn["confirmed-round"]
                )
            )
        except Exception as err:
            print(err)

        # res = self._algo_app.call(
        #     EmissionControl.business_opt_into_asset,
        #     business_address=business_address,
        #     asset_id=asset_id,
        #     suggested_params=sp,
        #     accounts=[business_address],
        #     foreign_assets=[asset_id],
        # )
        # self.print_txn(res)
        # return res

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
            EmissionControl.allocate_compliance_nft_to_business,
            business_address=business_address,
            asset_id=asset_id,
            suggested_params=sp,
            accounts=[business_address],
            foreign_assets=[asset_id],
        )
        self.print_txn(res)
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


def print_menu():
    print("--- CHOOSE FROM THE MENU OPTION BELOW ---")
    print(
        "1. Create an Emission Control for Carbon Dioxide (max emission: 100)"
    )
    print("2. Show the Emission Control Values configured for the app")
    print("3. Update the Carbon Dioxide Emission Control value to 200")
    print(
        "4. Check if Business1 is compliant with Carbon Dioxide Emission Control (emission value for Business1 is: 90)"
    )
    print(
        "5. Check if Business2 is compliant with Carbon Dioxide Emission Control (emission value for Business2 is: 220)"
    )
    print("6. Create a Compliance NFT")
    print("7. Make Business1 Opt into the Compliance NFT")
    print("8. Transfer Compliance NFT to Business1")
    print("0. Press 0 to Exit")


def update_app_id_in_storage(app_id):
    with open(EMISSION_CONTROL_FILE, "w") as fp:
        fp.write(str(app_id))


def get_app_id_in_storage() -> int:
    try:
        with open(EMISSION_CONTROL_FILE, "r") as fp:
            app_id = fp.read()
        return int(app_id)
    except Exception:
        return 0


def update_asset_id_in_storage(asset_id):
    with open(EMISSION_CONTROL_ASSET_FILE, "w") as fp:
        fp.write(str(asset_id))


def get_asset_id_in_storage() -> int:
    try:
        with open(EMISSION_CONTROL_ASSET_FILE, "r") as fp:
            asset_id = fp.read()
        return int(asset_id)
    except Exception:
        return 0


if __name__ == "__main__":
    print(
        "--- Starting Emission Control App Interaction with the python client ---"
    )
    print("--- See .emission_control file for verbose details ---")

    app_data = {}
    _client = None
    # Create the file before starting the process
    em_ctrl_file = Path(EMISSION_CONTROL_FILE)
    if not em_ctrl_file.exists():
        with open(EMISSION_CONTROL_FILE, "w") as fp:
            pass

    em_ctrl_asset_file = Path(EMISSION_CONTROL_ASSET_FILE)
    if not em_ctrl_asset_file.exists():
        with open(EMISSION_CONTROL_ASSET_FILE, "w") as fp:
            pass

    app_id = get_app_id_in_storage()
    asset_id = get_asset_id_in_storage()
    loop_break = False
    while True:
        if loop_break:
            break

        print_menu()
        try:
            input_val = input("\n--- INPUT YOUR CHOICE: ")
            if int(input_val) == 0:
                print("--- BYE. THANK YOU!")
                break
            elif int(input_val) == 1:
                _client = EmissionControlClient(app_id)
                update_app_id_in_storage(_client.get_app_id())
                _client.get_application_state()
                continue
            elif int(input_val) == 2:
                _client = EmissionControlClient(get_app_id_in_storage())
                _client.get_application_state()
                continue
            elif int(input_val) == 3:
                _client = EmissionControlClient(get_app_id_in_storage())
                _client.set_emissions_rule("CO2:Carbon Dioxide Emission", 200)
                continue
            elif int(input_val) == 4:
                _client = EmissionControlClient(get_app_id_in_storage())
                _client.is_business_compliant(
                    "CO2:Carbon Dioxide Emission", 90
                )
                continue
            elif int(input_val) == 5:
                _client = EmissionControlClient(get_app_id_in_storage())
                _client.is_business_compliant(
                    "CO2:Carbon Dioxide Emission", 220
                )
                continue
            elif int(input_val) == 6:
                _client = EmissionControlClient(get_app_id_in_storage())
                res = _client.create_compliance_token()
                update_asset_id_in_storage(res.return_value)
                continue
            elif int(input_val) == 7:
                _client = EmissionControlClient(get_app_id_in_storage())
                _client.opt_into_compliance_nft(
                    BUSINESS1_ACCOUNT_ADDRESS, get_asset_id_in_storage()
                )
                # update_asset_id_in_storage(res.return_value)
                continue
            elif int(input_val) == 8:
                _client = EmissionControlClient(get_app_id_in_storage())
                res = _client.transfer_compliance_token_to_business(
                    BUSINESS1_ACCOUNT_ADDRESS, get_asset_id_in_storage()
                )
                # update_asset_id_in_storage(res.return_value)
                continue

        except Exception:
            import traceback

            traceback.print_exc()
            print("--- INVALID INPUT. TRY AGAIN...")
            break
            # continue
