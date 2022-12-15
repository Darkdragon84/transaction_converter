from enum import Enum
from itertools import product

PAIR_CON = "-"


class TransactionType(Enum):
    WITHDRAW = "withdraw"
    DEPOSIT = "deposit"
    BUY = "buy"
    SELL = "sell"
    SWAP = "swap"
    FEE = "fee"
    EARN = "earn"
    PAY = "pay"


class Token(Enum):
    ALGO = "ALGO"
    ATOM = "ATOM"
    BNB = "BNB"
    BTC = "BTC"
    ETH = "ETH"
    DFI = "DFI"
    USDT = "USDT"


TOKENS = [str(token.value) for token in Token]
PAIRS = [PAIR_CON.join([t1, t2]) for t1, t2 in product(TOKENS, TOKENS) if t1 != t2]
ASSETS = TOKENS + PAIRS


class Exchange(Enum):
    Bitpanda = "Bitpanda"
    CakeDeFi = "CakeDeFi"
    Haru = "Haru"
