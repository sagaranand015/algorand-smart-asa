from typing import Final
from constants import COMPLIANCE_NFT_BASE_URL

from pyteal import *
from beaker import *


class EmissionRuleResult(abi.NamedTuple):
    emission: abi.Field[abi.String]
    max: abi.Field[abi.Uint64]
    min: abi.Field[abi.Uint64]


COMPLIANCE_ASA_APP_BINDING = COMPLIANCE_NFT_BASE_URL

UNDERLYING_COMPLIANCE_NFT_DECIMALS = Int(0)
UNDERLYING_COMPLIANCE_NFT_DEFAULT_FROZEN = Int(0)
UNDERLYING_COMPLIANCE_NFT_UNIT_NAME = Bytes("COM-ASA")
UNDERLYING_COMPLIANCE_NFT_NAME = Bytes("COMPLIANCE-ASA")
UNDERLYING_COMPLIANCE_NFT_URL = Bytes(COMPLIANCE_ASA_APP_BINDING)
UNDERLYING_COMPLIANCE_NFT_METADATA_HASH = Bytes("Comliance NFT Metadata")
UNDERLYING_COMPLIANCE_NFT_MANAGER_ADDR = Global.current_application_address()
UNDERLYING_COMPLIANCE_NFT_RESERVE_ADDR = Global.current_application_address()
UNDERLYING_COMPLIANCE_NFT_FREEZE_ADDR = Global.current_application_address()
UNDERLYING_COMPLIANCE_NFT_CLAWBACK_ADDR = Global.current_application_address()


class EmissionControl(Application):
    """
    Emission Control(aka Smart Contract App) for storing business' compliance analysis on chain
    and creating/minting NFTs for businesses based on the rules defined by the regulators.
    """

    regulator: Final[ApplicationStateValue] = ApplicationStateValue(
        TealType.bytes,
        descr="Regulator acting as the owner of the Emission Control",
    )
    emission_parameter: Final[ApplicationStateValue] = ApplicationStateValue(
        TealType.bytes, descr="Emission Parameter to keep track of"
    )
    emission_max: Final[ApplicationStateValue] = ApplicationStateValue(
        TealType.uint64, descr="Max value of the emission control parameter"
    )
    emission_min: Final[ApplicationStateValue] = ApplicationStateValue(
        TealType.uint64, descr="Min value of the emission control parameter"
    )

    @external
    def get_emission_rule(self, *, output: EmissionRuleResult):
        """
        Returns the rules defined by the regulator for the given emission SC
        """
        return Seq(
            (max := abi.Uint64()).set(self.emission_max.get()),
            (min := abi.Uint64()).set(self.emission_min.get()),
            (parameter := abi.String()).set(self.emission_parameter.get()),
            output.set(parameter, max, min),
        )

    @external
    def set_emission_rule(
        self,
        emission_parameter: abi.String,
        emission_max: abi.Uint64,
        emission_min: abi.Uint64,
        *,
        output: abi.Bool,
    ):
        """
        Sets the rules defined by the regulator for the given emission
        """
        return Seq(
            self.emission_parameter.set(emission_parameter.get()),
            self.emission_max.set(emission_max.get()),
            self.emission_min.set(emission_min.get()),
            output.set(True),
        )

    @external
    def is_business_compliant(
        self,
        emission_parameter: abi.String,
        emission_value: abi.Uint64,
        *,
        output: abi.Bool,
    ):
        """
        Returns true/false based on whether the business is compliant to the emissions value or not
        """
        return Seq(
            Assert(
                self.emission_parameter == emission_parameter.get(),
                comment="Emission Parameter given is not correct for the app being used!",
            ),
            Assert(
                emission_value.get() >= self.emission_min,
                comment="Emission value is lesser than min configured",
            ),
            If(emission_value.get() <= self.emission_max)
            .Then(output.set(True))
            .Else(output.set(False)),
        )

    @internal(TealType.uint64)
    def create_compliance_nft_internal(self):
        return Seq(
            InnerTxnBuilder.Begin(),
            InnerTxnBuilder.SetFields(
                {
                    TxnField.fee: Int(0),
                    TxnField.type_enum: TxnType.AssetConfig,
                    TxnField.config_asset_total: Int(1),
                    TxnField.config_asset_decimals: UNDERLYING_COMPLIANCE_NFT_DECIMALS,
                    TxnField.config_asset_unit_name: UNDERLYING_COMPLIANCE_NFT_UNIT_NAME,
                    TxnField.config_asset_name: UNDERLYING_COMPLIANCE_NFT_NAME,
                    TxnField.config_asset_url: UNDERLYING_COMPLIANCE_NFT_URL,
                    TxnField.config_asset_manager: UNDERLYING_COMPLIANCE_NFT_MANAGER_ADDR,
                    TxnField.config_asset_reserve: UNDERLYING_COMPLIANCE_NFT_RESERVE_ADDR,
                    TxnField.config_asset_freeze: UNDERLYING_COMPLIANCE_NFT_FREEZE_ADDR,
                    TxnField.config_asset_clawback: UNDERLYING_COMPLIANCE_NFT_CLAWBACK_ADDR,
                }
            ),
            InnerTxnBuilder.Submit(),
            Return(InnerTxn.created_asset_id()),
        )

    @internal(TealType.none)
    def app_opt_into_asset(self, asset_id: Expr):
        return Seq(
            InnerTxnBuilder.Begin(),
            InnerTxnBuilder.SetFields(
                {
                    TxnField.fee: Int(0),
                    TxnField.type_enum: TxnType.AssetTransfer,
                    TxnField.xfer_asset: asset_id,
                    TxnField.asset_amount: Int(1),
                    TxnField.sender: Global.current_application_address(),
                    # TxnField.asset_sender: Global.current_application_address(),
                    TxnField.asset_receiver: Global.current_application_address(),
                }
            ),
            InnerTxnBuilder.Submit(),
        )

    @internal(TealType.none)
    def transfer_compliance_nft_to_business(
        self, business_address: Expr, asset_id: Expr
    ):
        return Seq(
            InnerTxnBuilder.Begin(),
            InnerTxnBuilder.SetFields(
                {
                    TxnField.fee: Int(0),
                    TxnField.type_enum: TxnType.AssetTransfer,
                    TxnField.xfer_asset: asset_id,
                    TxnField.asset_amount: Int(1),
                    TxnField.sender: Global.current_application_address(),
                    # TxnField.asset_sender: Global.current_application_address(),
                    TxnField.asset_receiver: business_address,
                }
            ),
            InnerTxnBuilder.Submit(),
        )

    @external
    def create_compliance_nft(
        self, *, output: abi.Uint64
    ):
        """
        Creates the compliance NFT for the business via the Algorand SC
        """
        return Seq(
            (asset_id := abi.Uint64()).set(
                self.create_compliance_nft_internal()
            ),
            self.app_opt_into_asset(asset_id.get()),
            output.set(asset_id),
        )

    @external
    def allocate_compliance_nft_to_business(
        self,
        business_address: abi.Address,
        asset_id: abi.Uint64,
        *,
        output: abi.Uint64,
    ):
        """
        Creates the compliance NFT for the business via the Algorand SC
        """
        return Seq(
            self.transfer_compliance_nft_to_business(
                business_address.get(), asset_id.get()
            ),
            output.set(asset_id),
        )

    @create
    def create(self):
        return self.initialize_application_state()

    @update(authorize=Authorize.only(Global.creator_address()))
    def update(self):
        return Approve()

    @opt_in
    def opt_in(self):
        return Approve()


if __name__ == "__main__":
    EmissionControl().dump("./artifacts")
