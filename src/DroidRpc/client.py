# Python client for connecting to LORA Technologies' bot services

__author__ = "LORA Technologies"
__email__ = "asklora@loratechai.com"

from io import BytesIO
from google.protobuf.json_format import MessageToDict
from typing import Optional, List
import grpc
from .grpc_interface import bot_pb2_grpc, bot_pb2
from datetime import datetime
from .converter import datetime_to_timestamp
from .dataclasses import create_inputs, hedge_inputs, stop_inputs
from dataclasses import asdict
import math
import numpy as np
import json
from timeit import default_timer as timer
from datetime import timedelta

# TODO use pydantic dataclass to validate field types.

class Client:
    def __init__(self, address: str = "guardian", port: str = "50065"):
        self.address = address
        self.port = port
        self.channel = grpc.insecure_channel(self.address + ":" + self.port)
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
        response = self.droid.CreateBot(
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
        input_matrix: np.array
    ):
        """
        Generator function to be passed to the create_bots() gRPC bistream function.
        Splits a matrix of inputs into sub-batches and streams these sub-batches to Droid.

        Args:
            input_matrix (np.array(9,1)): List of inputs for each bot. The format is each row corresponds to the BatchCreate protobuf message.
        """


        # Split input matrix into smaller batches
        batch_size = 400
        splits = math.ceil(input_matrix.shape[1]/batch_size)
        input_matrix = np.array_split(input_matrix, splits, axis=1)

        for i, batch in enumerate(input_matrix):
            # Convert to Bytes
            start = timer()
            tickers_bytes = BytesIO()
            np.save(tickers_bytes, batch[0].astype('U7'), allow_pickle=False)
            spot_dates_bytes = BytesIO()
            np.save(spot_dates_bytes, batch[1].astype(np.datetime64), allow_pickle=False)
            investment_amounts_bytes = BytesIO()
            np.save(investment_amounts_bytes, batch[2].astype(float), allow_pickle=False)
            prices_bytes = BytesIO()
            np.save(prices_bytes, batch[3].astype(float), allow_pickle=False)
            bot_ids_bytes = BytesIO()
            np.save(bot_ids_bytes, batch[4].astype(str), allow_pickle=False)
            margins_bytes = BytesIO()
            np.save(margins_bytes, batch[5].astype(float), allow_pickle=False)
            fractionalss_bytes = BytesIO()
            np.save(fractionalss_bytes, batch[6].astype(bool), allow_pickle=False)
            tp_multipliers_bytes = BytesIO()
            np.save(tp_multipliers_bytes, batch[7].astype(float), allow_pickle=False)
            sl_multipliers_bytes = BytesIO()
            np.save(sl_multipliers_bytes, batch[8].astype(float), allow_pickle=False)

            print(f"Byte conversion time (msg {i}): {timedelta(seconds=(timer()-start))}")

            message = bot_pb2.BatchCreate(
                tickers=tickers_bytes.getvalue(),
                spot_dates=spot_dates_bytes.getvalue(),
                investment_amounts=investment_amounts_bytes.getvalue(),
                prices=prices_bytes.getvalue(),
                bot_ids=bot_ids_bytes.getvalue(),
                margins=margins_bytes.getvalue(),
                fractions=fractionalss_bytes.getvalue(),
                tp_multipliers=tp_multipliers_bytes.getvalue(),
                sl_multipliers=sl_multipliers_bytes.getvalue()
            )
            # print(message.__sizeof__())

            yield message
    
    def create_bots(
        self,
        bot_inputs: List[create_inputs]
    ):
        """
        Returns a list of bots as dictionaries.

        Args:
            bot_inputs (List[create_inputs]): Inputs for bot creation.

        Returns:
            Generator: Generator of responses from Droid.
        """
        input_types = np.dtype([
            ('ticker', 'U7'),
            ('spot_date', str),
            ('investment_amount', float),
            ('price', float),
            ('bot_id', str),
            ('margin', float),
            ('fraction', bool),
            ('tp_multiplier', float),
            ('sl_multiplier', float)])

        # Convert the inputs into numpy arrays
        # TODO: pipeline this so that batches of numpy arrays are constructed as streaming is happening. Right now we need to wait for all inputs to be converted.
        start = timer()
        input_matrix = np.empty([1,9])
        for i in bot_inputs:
            arr = np.array([[
                i.ticker,
                np.datetime64(i.spot_date),
                i.investment_amount,
                i.price,
                i.bot_id,
                i.margin,
                i.fractionals,
                i.tp_multiplier,
                i.sl_multiplier
            ]])
            input_matrix = np.concatenate((input_matrix, arr))
        input_matrix = np.delete(input_matrix, 0, 0)
        print(f"Total Numpy Conversion time: {timedelta(seconds=(timer()-start))}")

        # Rotate matrix
        input_matrix = np.rot90(input_matrix, k=-1)

        # Send over gRPC
        # TODO: Use a secure channel, since this is external facing
        responses = self.droid.CreateBots(self.__create_bot_generator(input_matrix))

        # Returning a list would be easier for client to work with, but they would have to wait for all bots to be created.
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
        response = self.droid.HedgeBot(
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
        response = self.droid.StopBot(
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
        
