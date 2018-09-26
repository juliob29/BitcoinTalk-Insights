# -*- coding: utf-8 -*-
"""
Tests for the Crypto class.
"""
import os 
import plotly
import unittest
from isoweek import Week
from skill.skill import Crypto
from tests.data import article_data


class CryptoTestCase(unittest.TestCase):
    """
    Test case for the Crypto() class.
    """

    @classmethod
    def setUpClass(self):
        """
        Method that instantiate the Test Case.
        """
        
        self.skill = Crypto()

    
    def test_skill_Crypto_results(self):
        """
        Crypto().text() gives a numberic output.
        """
        try:
            results = Crypto().text(
                text=article_data, limit=3)
            assert len(results) > 0
            for result in results:
                assert 'id' in result.keys()
                assert 'matches' in result.keys()
                assert 'prices' in result.keys()
                assert 'chart' in result.keys()
                assert 'related' in result.keys()
        except plotly.exceptions.PlotlyRequestError:
            pass

    def test_skill_Crypto_regex_plural(self):
        """
        Crypto().text() classifies the same coin, with different starts and ends
        even if its plural.
        """
        try:
            results = Crypto().text(
                'bitcoin bitcoins', limit=3)
            for result in results:
                assert len(results) > 0
                assert result['matches'][0]['name_start'] == 0
                assert result['matches'][0]['name_end'] == 7
                assert result['matches'][1]['name_start'] == 8
                assert result['matches'][1]['name_end'] == 16
        except plotly.exceptions.PlotlyRequestError:
            pass

    def test_skill_crypto_symbol_is_correctly_identified(self):
        """
        Crypto().text() classifies the same coin, with different starts and ends
        even if both classifications are different (name and symbol).
        """
        results = Crypto().text('bitcoin BTC', limit=3)
        for result in results:
            assert len(results) > 0
            assert result['matches'][0]['name_start'] == 0
            assert result['matches'][0]['name_end'] == 7
            assert result['matches'][1]['name_start'] == 8
            assert result['matches'][1]['name_end'] == 11
            
    def test_no_conversation_about_coin(self):
        results = Crypto().text('Fluttercoin', limit=3)
        for result in results:
            assert len(results) > 0
            assert result['related'] == []

    def test_different_limits_different_results(self):
        """
        Crypto().text() limit paramater limits the length of the output object
        to the integer given.
        """
        results = self.skill.text(text=article_data, limit=3)
        assert len(results) == 3

        results = self.skill.text(text=article_data, limit=1)
        assert len(results) == 1
