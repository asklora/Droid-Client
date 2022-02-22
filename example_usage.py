# Example usage of this package

__author__ = "LORA Technologies"
__email__ = "asklora@loratechai.com"

from LoraDroidClient import Client
from pprint import pprint

client = Client(address='<HOST>', port='50065')
create_response = client.create_bot(
    ticker            = "IBM",                 # RIC code
    spot_date         = "2022-02-15",          # 
    investment_amount = 100000,                # 
    price             = 156.5,                 # Optional for demo
    bot_id            = "CLASSIC_classic_025", # ID of bot type
    margin            = 1,                     # (Optional) How much margin to use
    fractionals       = False,                 # Whether to use fractional shares
)

pprint(create_response)
print()

hedge_response = client.hedge(
    create_response['bot_id'],
    create_response['ticker'],
    170,
    create_response['entry_price']+5,
    create_response['share_num'],
    create_response.get('delta',0),
    100000,
    100000 - (create_response['share_num']*create_response['entry_price']),
    create_response['max_loss_price'],
    create_response['target_profit_price'],
    create_response['expiry'],
    strike=create_response.get('strike',0),
    strike_2 = create_response.get('strike_2',0),
    barrier = create_response.get('barrier',0),
    option_price=create_response.get('option_price',0),
)
pprint(hedge_response)
print()

stop_response = client.stop(
    create_response['bot_id'],
    create_response['ticker'],
    155.4,
    create_response['entry_price'],
    create_response['share_num'],
    create_response.get('delta',0),
    100000,
    100000 - (create_response['share_num']*create_response['entry_price']),
    create_response['max_loss_price'],
    create_response['target_profit_price'],
    create_response['expiry'],
    strike=create_response.get('strike',0),
    strike_2 = create_response.get('strike_2',0),
    barrier = create_response.get('barrier',0),
    option_price=create_response.get('option_price',0),
)
pprint(stop_response)
print()
