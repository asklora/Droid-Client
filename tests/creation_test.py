# Bot creation test

__author__ = "LORA Technologies"
__email__ = "asklora@loratechai.com"

import pytest
from DroidRpc import Client

class InputGenerator:
    """
    Contains functions that generate inputs for testing bot creation.
    """
    @classmethod
    def create_inputs(
            cls,
            ticker            = "IBM",
            spot_date         = "2022-02-15",
            investment_amount = 100000,
            price             = 156.5,
            bot_id            = "CLASSIC_classic_025",
            margin            = 1,
            fractionals       = False,
        ):
        """
        Returns a dict of inputs to pass to droid w/ default values.
        """
        inputs = {
            "ticker"            : ticker,
            "spot_date"         : spot_date,
            "investment_amount" : investment_amount,
            "price"             : price,
            "bot_id"            : bot_id,
            "margin"            : margin,
            "fractionals"       : fractionals,
        }
        return inputs

    @classmethod
    def create_missing_field_inputs(cls):
        """
        Returns a a tuple of inputs and expected values, where each set of inputs has one missing field.
        """
        input_collection = []
        baseInputs = cls.create_inputs()
        for arg in baseInputs:
            if arg == "price":
                expected = "PASS"
            elif arg == "margin":
                expected = "PASS"
            elif arg == "fractionals":
                expected = "PASS"
            else:
                expected = TypeError
            inputs = baseInputs.copy()
            inputs.pop(arg)
            input_collection.append(({'missing_field': arg, 'inputs': inputs}, expected))
        return input_collection


class TestBotCreation:
    bots = [] # Holds created bots.
    client = Client(address='47.242.41.160')

    def check_bot_valid(self, bot_response):
        """
        Checks if the bot creation response is valid.

        Args:
            bot_response (dict): The response generated be the LORA Bot service.

        Returns:
            bool: If the reponse is valid
        """
        # TODO This will need to be expanded to be more robust.
        expected_format = {
            'ticker': str,
            'share_num': str,
            'expiry': str,
            'spot_date': str,
            'created': str,
            'total_bot_share_num': str,
            'max_loss_pct': str,
            'max_loss_price': str,
            'max_loss_amount': str,
            'target_profit_pct': str,
            'target_profit_price': str,
            'target_profit_amount': str,
            'entry_price': str,
            'margin': str,
            'bot_id': str,
            'fraction': str,
            'side': str,
            'status': str,
            'vol': str,
            'classic_vol': str,
            'strike_2': str,
            'barrier': str,
            'delta': str,
            'option_price': str,
            'q': str,
            'r': str,
            'strike': str,
            't': str,
            'v1': str,
            'v2': str,
            }
        if not isinstance(bot_response, dict): return False
        if bot_response.keys() != expected_format.keys(): return False
        for field in bot_response:
            if not isinstance(field, expected_format[field]): return False

        return True

    def test_successful_creation(self):
        """
        Test that the creation succeeds
        """
        # TODO Test more valid inputs
        bot1 = self.client.create_bot(**InputGenerator.create_inputs())
        self.bots.append(bot1)
        for bot in self.bots:
            assert self.check_bot_valid(bot)

    @pytest.mark.parametrize("inputs, expected", InputGenerator.create_missing_field_inputs())
    def test_missing_fields(self, inputs, expected):
        """
        Test error handling for missing fields.
        """
        if expected == "PASS":
            assert self.check_bot_valid(self.client.create_bot(**inputs['inputs']))
        else:
            with pytest.raises(expected):
                self.client.create_bot(**inputs['inputs'])

    @pytest.mark.skip(reason="Test not yet written")
    def test_incorrect_field_type(self):
        """
        Test error handling of incorrect input field types
        """
        # TODO
        pass

    @pytest.mark.skip(reason="Test not yet written")
    def test_big_inputs(self):
        """
        Test how the client handles big inputs
        """
        # TODO
        pass

    @pytest.mark.skip(reason="Test not yet written")
    def test_null_value(self):
        """
        Test error handliong for None types being passed
        """
        # TODO
        pass
