from abc import ABC, abstractmethod
from pathlib import Path
from typing import Union, Optional, Iterator
import pandas as pd

from constants import Exchange, ASSETS


class ExportedTransaction(ABC):
    EXCHANGE: Optional[Exchange] = None
    COLUMNS: list[str] = []
    DATE: str = "Date"
    AMOUNT: str = "Amount"
    ASSET: str = "Asset"
    TRANSACTION_TYPE: str = "Transaction Type"
    TRANSACTION_ID: str = "Transaction ID"

    def __init__(self, csv_file: str | Path):
        self.csv_file = csv_file
        self.dataframe: pd.DataFrame = pd.read_csv(self.csv_file).fillna("")
        self.dataframe[self.DATE] = pd.to_datetime(self.dataframe[self.DATE])
        self.dataframe.index = self.dataframe[self.TRANSACTION_ID]

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

    @property
    @abstractmethod
    def outgoing(self) -> pd.DataFrame:
        pass


class CakeExportedTransactions(ExportedTransaction):
    EXCHANGE = Exchange.CakeDeFi
    ASSET = "Coin/Asset"
    TRANSACTION_TYPE = "Operation"
    TRANSACTION_ID = "Reference"
    RELATED_TRANSACTION_ID = "Related reference ID"

    COLUMNS = [
        ExportedTransaction.DATE,
        TRANSACTION_TYPE,
        ExportedTransaction.AMOUNT,
        ASSET,
        "FIAT value",
        "FIAT currency",
        "Transaction ID",
        "Withdrawal address",
        TRANSACTION_ID,
        "Related reference ID"
    ]

    def __init__(self, csv_file: Union[str, Path]):
        super().__init__(csv_file)

    @property
    def ingoing_mask(self)-> pd.DataFrame:
        return self.dataframe[self.AMOUNT] > 0

    @property
    def outgoing_mask(self) -> pd.DataFrame:
        return self.dataframe[self.AMOUNT] < 0

    def _masked_transactions(self, mask: pd.DataFrame) -> pd.DataFrame:
        df_masked = self.dataframe[mask]
        return df_masked[[self.DATE, self.ASSET, self.AMOUNT]]

    @property
    def ingoing(self) -> pd.DataFrame:
        return self._masked_transactions(self.ingoing_mask)

    @property
    def outgoing(self) -> pd.DataFrame:
        return self._masked_transactions(self.outgoing_mask)

    @property
    def related_transactions(self) -> Iterator[tuple[pd.Series, pd.Series]]:
        for _, row in self.dataframe.iterrows():

            related_id = row[self.RELATED_TRANSACTION_ID]
            if not related_id:
                continue
            try:
                related = self.dataframe.loc[related_id]
                yield row, related
            except KeyError:
                print(f"no reference {related_id}")
                pass
