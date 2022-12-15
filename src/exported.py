from abc import ABC, abstractmethod
from pathlib import Path
from typing import Union, Optional
import pandas as pd

from constants import Exchange, Asset, ASSETS


class ExportedTransaction(ABC):
    EXCHANGE: Optional[Exchange] = None
    COLUMNS: list[str] = []
    DATE: str = "Date"
    AMOUNT: str = "Amount"
    ASSET: str = "Asset"
    TRANSACTION_TYPE: str = "Transaction Type"

    def __init__(self, csv_file: str | Path):
        self.csv_file = csv_file
        self.dataframe: pd.DataFrame = pd.read_csv(self.csv_file).fillna("")
        self.dataframe[self.DATE] = pd.to_datetime(self.dataframe[self.DATE])

        if self.dataframe.columns.tolist() != self.COLUMNS:
            raise ValueError(f"Imported CSV has columns {self.dataframe.columns.tolist()} "
                             f"but {self.__class__.__name__} expected {self.COLUMNS}")

        unknown = set(self.dataframe[self.ASSET]) - set(ASSETS)
        if unknown:
            print(f"unknown currencies: {unknown}")

    @property
    @abstractmethod
    def ingoing(self) -> pd.DataFrame:
        pass

    # @property
    # @abstractmethod
    # def outgoing(self) -> pd.DataFrame:
    #     pass


class CakeExportedTransactions(ExportedTransaction):
    EXCHANGE = Exchange.DeFiCake
    ASSET = "Coin/Asset"
    TRANSACTION_TYPE = "Operation"

    COLUMNS = [
        ExportedTransaction.DATE,
        TRANSACTION_TYPE,
        ExportedTransaction.AMOUNT,
        ASSET,
        "FIAT value",
        "FIAT currency",
        "Transaction ID",
        "Withdrawal address",
        "Reference",
        "Related reference ID"
    ]

    def __init__(self, csv_file: Union[str, Path]):
        super().__init__(csv_file)
        # self.dataframe = self.dataframe.rename({"Operation": self.TRANSACTION_TYPE, "Coin/Asset": self.ASSET})

    @property
    def ingoing_mask(self):
        return self.dataframe[self.AMOUNT] > 0

    @property
    def outgoing_mask(self):
        return self.dataframe[self.AMOUNT] < 0

    def _masked_transactions(self, mask) -> pd.DataFrame:
        df_masked = self.dataframe[mask]
        return df_masked[[self.DATE, self.ASSET, self.AMOUNT]]

    @property
    def ingoing(self):
        return self._masked_transactions(self.ingoing_mask)

    @property
    def outgoing(self):
        return self._masked_transactions(self.outgoing_mask)
