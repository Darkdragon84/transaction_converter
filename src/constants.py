from enum import Enum


class Asset(Enum):
    ALGO = "ALGO"
    ATOM = "ATOM"
    BNB = "BNB"
    BTC = "BTC"
    ETH = "ETH"
    BTCDFI = "BTC-DFI"
    DFI = "DFI"


ASSETS = [asset.value for asset in Asset]


class Exchange(Enum):
    Bitpanda = "Bitpanda"
    DeFiCake = "DeFiCake"
    Haru = "Haru"
