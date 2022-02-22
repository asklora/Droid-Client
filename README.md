# LORA Technologies Bot Client
Client for LORA Tech's bot services.

**Example**  
A working example script that you can try can be found at https://github.com/asklora/Droid-Client/blob/production/example_usage.py


## Usage:  
### Bot Creation
```
Client.create_bot(args, **kwargs)

Args:
    ticker (str): cRIC code for which stock to create a bot for
    spot_date (str): Date for bot creations.
    investment_amount (float): Amount of cash the bot can use.
    bot_id (str): The type of bot to use (e.g. CLASSIC_classic_025)

Kwargs:
    margin (int): Amount of margin the bot is allowed to use. Defaults to 1.
    price (float): Price of the stock (any currency). Defaults to None (current price).
    fractionals (bool): Whether the bot should use fractional shares. Defaults to False.

Returns:
    dict: Parsed bot service response.
        {
            ticker (str),                 # RIC code
            share_num (float),            # Number of shares bought
            expiry (str),                 # Date of expiry
            spot_date (str),              # [For internal use]
            created (str),                # Date of bot creation
            total_bot_share_num (int),    # Number of shares held by this bot
            max_loss_pct (float),         # 
            max_loss_price (float),       # 
            max_loss_amount (float),      # 
            target_profit_pct (float),    # 
            target_profit_price (float),  # 
            target_profit_amount (float), # 
            entry_price (float),          # Price of stock when this bot was created
            margin (int),                 # Amount of margin this bot is allowed to use
            bot_id (str),                 # This bot's bot type
            fractionals (bool),           # Whether this bot is allowed to use fractional shares
            side (str),                   # 
            status (str),                 # Status of this bot (i.e. active)
            vol (float),                  # 
            classic_vol (float),          # 
            strike_2 (int),               # 
            barrier (int),                # 
            delta (int),                  # 
            option_price (int),           # 
            q (int),                      # 
            r (int),                      # 
            strike (int),                 # 
            t (int),                      # 
            v1 (int),                     # 
            v2 (int),                     # 
        }
```

### Hedging using an existing bot
```
Client.hedge(*args, **kwargs)

Args:
    bot_id (str): Type of bot.
    ticker (str): RIC code.
    current_price (float): Current price (any currency).
    entry_price (float): Price when the bot was created.
    last_share_num (float): Number of shares currently held by the bot.
    last_hedge_delta (float): Number of shares last sold/bought by the bot.
    investment_amount (float): Total cash value the bot is allowed to manage.
    bot_cash_balance (float): Remaining cash the bot has.
    stop_loss_price (float): Stop loss level of the bot.
    take_profit_price (float): Take profit level of the bot.
    expiry (str): Date when the bot expires.

Kwargs:
    strike (Optional[float]): _description_. Defaults to None.
    strike_2 (Optional[float]): _description_. Defaults to None.
    margin (Optional[int]): Amount of margin the bot can use. Defaults to 1.
    fractionals (Optional[bool]): Whether this bot is allowed to use fractional shares. Defaults to False.
    option_price (Optional[float]): _description_. Defaults to None.
    barrier (Optional[float]): _description_. Defaults to None.
    current_low_price (Optional[float]): _description_. Defaults to None.
    current_high_price (Optional[float]): _description_. Defaults to None.
    ask_price (Optional[float]): _description_. Defaults to None.
    bid_price (Optional[float]): _description_. Defaults to None.
    trading_day (Optional[str]): _description_. Defaults to datetime.strftime(datetime.now().date(), "%Y-%m-%d  ").

Returns:
    dict: Parsed bot service response
        {
            entry_price (float),       # 
            current_price (float),     # Current price of stock
            share_num (float),         # 
            total_bot_share_num (int), # 
            last_hedge_delta (int),    # 
            share_change (int),        # 
            side (str),                # 
            status (str),              # 
            strike_2 (int),            # 
            barrier (int),             # 
            delta (int),               # 
            option_price (int),        # 
            q (int),                   # 
            r (int),                   # 
            strike (int),              # 
            t (int),                   # 
            v1 (int),                  # 
            v2 (int),                  # 
        }
```

### Stopping a bot
```
Client.stop(*args, **kwargs)

Args:
    bot_id (str): Type of bot.
    ticker (str): RIC code.
    current_price (float): Current price (any currency).
    entry_price (float): Price when the bot was created.
    last_share_num (float): Number of shares currently held by the bot.
    last_hedge_delta (float): Number of shares last sold/bought by the bot.
    investment_amount (float): Total cash value the bot is allowed to manage.
    bot_cash_balance (float): Remaining cash the bot has.
    stop_loss_price (float): Stop loss level of the bot.
    take_profit_price (float): Take profit level of the bot.
    expiry (str): Date when the bot expires.

Kwargs:
    strike (Optional[float]): _description_. Defaults to None.
    strike_2 (Optional[float]): _description_. Defaults to None.
    margin (Optional[int]): Amount of margin the bot can use. Defaults to 1.
    fractionals (Optional[bool]): Whether this bot is allowed to use fractional shares. Defaults to False.
    option_price (Optional[float]): _description_. Defaults to None.
    barrier (Optional[float]): _description_. Defaults to None.
    current_low_price (Optional[float]): _description_. Defaults to None.
    current_high_price (Optional[float]): _description_. Defaults to None.
    ask_price (Optional[float]): _description_. Defaults to None.
    bid_price (Optional[float]): _description_. Defaults to None.
    trading_day (Optional[str]): _description_. Defaults to datetime.strftime(datetime.now().date(), "%Y-%m-%d  ").

Returns:
    dict: Parsed bot service response
        {
            entry_price (float),       # 
            current_price (float),     # Current price of stock
            share_num (float),         # 
            total_bot_share_num (int), # 
            last_hedge_delta (int),    # 
            share_change (int),        # 
            side (str),                # 
            status (str),              # 
            strike_2 (int),            # 
            barrier (int),             # 
            delta (int),               # 
            option_price (int),        # 
            q (int),                   # 
            r (int),                   # 
            strike (int),              # 
            t (int),                   # 
            v1 (int),                  # 
            v2 (int),                  # 
        }
```
