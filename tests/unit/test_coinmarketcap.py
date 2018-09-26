# -*- coding: utf-8 -*-
"""
Tests for the Crypto class.
"""
import unittest

from datetime import datetime
from skill.coinmarketcap import CoinMarketCap


class CoinMarketCapTestCase(unittest.TestCase):
    """
    Test case for the CoinMarketCap() class.
    """
    @classmethod
    def setUpClass(self):
        """
        Method that instantiate the Test Case.
        """
        self.coin_market_cap = CoinMarketCap()

    def test_status_returns_boolean(self):
        """
        CoinMarketCap().status returns boolean.
        """
        assert isinstance(self.coin_market_cap.status, bool)
    
    def test_coin_ids_are_integers(self):
        """
        CoinMarketCap().coin_ids returns list of integers.
        """
        for coin_id in self.coin_market_cap.coin_ids:
            assert isinstance(coin_id, int)
        
    def test_coin_ids_are_strings(self):
        """
        CoinMarketCap().coin_ids returns list of strings.
        """
        for coin_id in self.coin_market_cap.coin_slugs:
            assert isinstance(coin_id, str)
    
    def test_historic_data_returns_correct_values(self):
        """
        CoinMarketCap().historic() returns correct values.
        """
        results = self.coin_market_cap.historic('bitcoin')
        for result in results:
            print(result)
            date = datetime.strptime(result['date'], '%Y-%m-%d')
            assert isinstance(date, datetime)

    def test_listings_return_list(self):
        """
        CoinMarketCap().listings() returns list of currencies.
        """
        results = self.coin_market_cap.listings()
        assert isinstance(results, list)

    def test_current_return_current_prices(self):
        """
        CoinMarketCap().current() returns current prices of cryptocurrency.
        """
        results = self.coin_market_cap.current(1)
        assert isinstance(results, dict)

    def test_raises_value_error_if_coin_doesnt_exist(self):
        """
        CoinMarketCap().current() raises ValueError if coin doesn't exist.
        """
        with self.assertRaises(ValueError):
            self.coin_market_cap.current('foobarcoin')
            
