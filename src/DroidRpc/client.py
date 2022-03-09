# Python client for connecting to LORA Technologies' bot services

__author__ = "LORA Technologies"
__email__ = "asklora@loratechai.com"

from google.protobuf.json_format import MessageToDict
from typing import Optional, List
import grpc
from .grpc_interface import bot_pb2_grpc, bot_pb2
from datetime import datetime
from .converter import datetime_to_timestamp
from .dataclasses import create_inputs, hedge_inputs, stop_inputs
from dataclasses import asdict
import json

# TODO use pydantic dataclass to validate field types.

class Client:
    def __init__(self, address: str = "guardian", port: str = "50065"):
        self.address = address
        self.port = port
        self.channel = grpc.insecure_channel(self.address + ":" + self.port)
        self.stub = bot_pb2_grpc.EchoStub(self.channel)
        self.droid = bot_pb2_grpc.DroidStub(self.channel) # This one contains the bistream

    def __string_to_datetime(self, date: str):
        date = datetime.strptime(date, "%Y-%m-%d")
        time = datetime.now().time()

        date_class = datetime_to_timestamp(datetime.combine(date, time))
        return date_class

    def create_bot(
        self,
        ticker: str,
        spot_date: str,
        investment_amount: float,
        bot_id: str,
        margin: int = 1,
        price: float = None,
        fractionals: bool = False,
        tp_multiplier: Optional[float] = None,
        sl_multiplier: Optional[float] = None
    ):
        response = self.stub.CreateBot(
            bot_pb2.Create(
                ticker=ticker,
                spot_date=self.__string_to_datetime(spot_date),
                investment_amount=investment_amount,
                price=price,
                bot_id=bot_id,
                margin=margin,
                fraction=fractionals,
                tp_multiplier=tp_multiplier,
                sl_multiplier=sl_multiplier
            )
        )
        return json.loads(response.message)

    def __create_bot_generator(
        self, 
        bot_inputs: List[create_inputs]
    ):
        """
        Generator function to be passed to the create_bots() gRPC bistream function.

        Args:
            bot_inputs (List): List of inputs for each bot. The
        """
        for i in bot_inputs:
            yield bot_pb2.Create(
                ticker=i.ticker,
                spot_date=self.__string_to_datetime(i.spot_date),
                investment_amount=i.investment_amount,
                price=i.price,
                bot_id=i.bot_id,
                margin=i.margin,
                fraction=i.fractionals,
                tp_multiplier=i.tp_multiplier,
                sl_multiplier=i.sl_multiplier
            )
    
    def create_bots(
        self,
        bot_inputs: List[create_inputs]
    ):
        """
        Returns a list of bots as dictionaries.

        Args:
            bot_inputs (List[create_inputs]): _description_

        Returns:
            _type_: _description_
        """
        # TODO: Use a secure channel, since this is external facing
        responses = self.droid.CreateBots(self.__create_bot_generator(bot_inputs))
        # Returning a list would be easier for client to work wtih, but they would have to wait for all bots to be created.
        # This is slow because they can't pipeline. I'm not sure what we want to do here.
        # return [MessageToDict(response) for response in responses]
        return responses


    def hedge(
        self,
        bot_id: str,
        ticker: str,
        current_price: float,
        entry_price: float,
        last_share_num: float,
        last_hedge_delta: float,
        investment_amount: float,
        bot_cash_balance: float,
        stop_loss_price: float,
        take_profit_price: float,
        expiry: str,
        strike: Optional[float] = None,
        strike_2: Optional[float] = None,
        margin: Optional[int] = 1,
        fractionals: Optional[bool] = False,
        option_price: Optional[float] = None,
        barrier: Optional[float] = None,
        current_low_price: Optional[float] = None,
        current_high_price: Optional[float] = None,
        ask_price: Optional[float] = None,
        bid_price: Optional[float] = None,
        trading_day: Optional[str] = datetime.strftime(datetime.now().date(), "%Y-%m-%d")
    ):
        response = self.stub.HedgeBot(
            bot_pb2.Hedge(
                ric=ticker,
                expiry=self.__string_to_datetime(expiry),
                investment_amount=investment_amount,
                current_price=current_price,
                bot_id=bot_id,
                margin=margin,
                entry_price=entry_price,
                last_share_num=last_share_num,
                last_hedge_delta=last_hedge_delta,
                bot_cash_balance=bot_cash_balance,
                stop_loss_price=stop_loss_price,
                take_profit_price=take_profit_price,
                option_price=option_price,
                strike=strike,
                strike_2=strike_2,
                barrier=barrier,
                current_low_price=current_low_price,
                current_high_price=current_high_price,
                ask_price=ask_price,
                bid_price=bid_price,
                fraction=fractionals,
                trading_day=self.__string_to_datetime(trading_day)
            )
        )
        return json.loads(response.message)
    
    def stop(
        self,
        bot_id: str,
        ticker: str,
        current_price: float,
        entry_price: float,
        last_share_num: float,
        last_hedge_delta: float,
        investment_amount: float,
        bot_cash_balance: float,
        stop_loss_price: float,
        take_profit_price: float,
        expiry: str,
        strike: Optional[float] = None,
        strike_2: Optional[float] = None,
        margin: Optional[int] = 1,
        fractionals: Optional[bool] = False,
        option_price: Optional[float] = None,
        barrier: Optional[float] = None,
        current_low_price: Optional[float] = None,
        current_high_price: Optional[float] = None,
        ask_price: Optional[float] = None,
        bid_price: Optional[float] = None,
        trading_day: Optional[str] = datetime.strftime(datetime.now().date(), "%Y-%m-%d")
    ):
        response = self.stub.StopBot(
            bot_pb2.Stop(
                ric=ticker,
                expiry=self.__string_to_datetime(expiry),
                investment_amount=investment_amount,
                current_price=current_price,
                bot_id=bot_id,
                margin=margin,
                entry_price=entry_price,
                last_share_num=last_share_num,
                last_hedge_delta=last_hedge_delta,
                bot_cash_balance=bot_cash_balance,
                stop_loss_price=stop_loss_price,
                take_profit_price=take_profit_price,
                option_price=option_price,
                strike=strike,
                strike_2=strike_2,
                barrier=barrier,
                current_low_price=current_low_price,
                current_high_price=current_high_price,
                ask_price=ask_price,
                bid_price=bid_price,
                fraction=fractionals,
                trading_day=self.__string_to_datetime(trading_day)
            )
        )
        return json.loads(response.message)
        
