# Contains the dataclasses used by the client generator function

from dataclasses import dataclass
from typing import Optional
from datetime import datetime


@dataclass
class create_inputs:
    ticker: str
    spot_date: str
    investment_amount: float
    bot_id: str
    current_price: Optional[float] = None
    margin: Optional[float] = 1
    fraction: Optional[bool] = False
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
    margin: float
    total_bot_share_num: float
    expire_date: str
    price_level_1: float
    price_level_2: float
    current_price: Optional[float] = None
    last_hedge_delta: Optional[float] = None
    last_share_num: Optional[float] = None
    bot_cash_balance: Optional[float] = None
    current_low_price: Optional[float] = None
    current_high_price: Optional[float] = None
    ask_price: Optional[float] = None
    bid_price: Optional[float] = None


@dataclass
class stop_inputs:
    ticker: str
    spot_date: str
    bot_id: str
    investment_amount: float
    margin: float
    total_bot_share_num: float
    expire_date: str
    price_level_1: float
    price_level_2: float
    current_price: Optional[float] = None
    last_hedge_delta: Optional[float] = None
    last_share_num: Optional[float] = None
    bot_cash_balance: Optional[float] = None
    current_low_price: Optional[float] = None
    current_high_price: Optional[float] = None
    ask_price: Optional[float] = None
    bid_price: Optional[float] = None
