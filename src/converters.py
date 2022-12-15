from abc import ABC, abstractmethod
from typing import TYPE_CHECKING
import pandas as pd

if TYPE_CHECKING:
    from exported import ExportedTransaction


class Converter(ABC):
    @classmethod
    @abstractmethod
    def convert(cls, exported: ExportedTransaction) -> pd.DataFrame:
        pass


class CoinStatsConverter(Converter):
    DATE_FORMAT = "%m/%d/%Y %I:%M:%S %p"

    @classmethod
    def convert(cls, exported: ExportedTransaction) -> pd.DataFrame:
        pass