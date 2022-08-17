# Contains the dataclasses used by the client generator function

from dataclasses import dataclass
from typing import Optional
from datetime import datetime


@dataclass
class create_inputs:
    ticker: str
    spot_date: str
    bot_id: str
    investment_amount: float
    ask_price: float
    bid_price: float
    margin: Optional[float] = None
    fraction: Optional[bool] = None
    multiplier_1: Optional[float] = None
    multiplier_2: Optional[float] = None


@dataclass
class hedge_inputs:
    """
    Beware of sequence here != protobuf input sequence (due to default values)
    """
    ticker: str
    spot_date: str
    bot_id: str
    investment_amount: float
    ask_price: float
    bid_price: float
    margin: float
    fraction: bool
    total_bot_share_num: float
    expire_date: str
    price_level_1: float
    price_level_2: float
    last_hedge_delta: Optional[float] = None
    last_share_num: Optional[float] = None
    bot_cash_balance: Optional[float] = None


@dataclass
class stop_inputs:
    ticker: str
    spot_date: str
    bot_id: str
    investment_amount: float
    ask_price: float
    bid_price: float
    margin: float
    fraction: bool
    total_bot_share_num: float
    expire_date: str
    price_level_1: float
    price_level_2: float
    last_hedge_delta: Optional[float] = None
    last_share_num: Optional[float] = None
    bot_cash_balance: Optional[float] = None
