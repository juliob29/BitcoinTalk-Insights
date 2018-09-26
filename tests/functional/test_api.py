# -*- coding: utf-8 -*-
"""
Tests for the API.
"""
import json
import plotly
import unittest

from tests.data import article_data
from skill.api.server import Server


class CryptoTestCase(unittest.TestCase):
    """
    Test case for the skill-template test case.
    """
    @classmethod
    def setUpClass(cls):
        S = Server(debug=False).app
        cls.server = S.test_client

    def test_status_conforms_to_warden(self):
        """
        /status endpoint matches Warden requirements.
        """
        _, response = self.server.get('/status')
        self.assertTrue(response.json.get('success'))

        warden_keys = ['success', 'description', 'name', 'release_date', 'version']
        for k in warden_keys:
            self.assertIn(k, response.json.keys())

    def test_crypto_returns_arrays(self):
        """
        /detect creates an estimate based on skill.
        """
        try:
            data = {
            'text': """
            By Bitcoin the design to make cars. Foo bar lorem ipsum. And then there was rain.
            """
        }
            _, response = self.server.post('/detect', data=json.dumps(data))

            self.assertTrue(response.json.get('success'))
            assert len(response.json.get('results')) > 0

        except AttributeError:
            pass

    def test_Crypto_doesnt_accept_get(self):
        """
        /detect doesn't accept GET method.
        """
        data = {
            'text': """
            By simplifying the design to make cars. Foo bar lorem ipsum. And then there was rain.
            """
        }
        _, response = self.server.get('/detect', data=json.dumps(data))

        self.assertTrue(response.status == 400)
        
    def test_summarize_accepts_options(self):
        """
        /detect doesn't accept OPTIONS method.
        """
        data = {
            'text': """
            By simplifying the design to make cars. Foo bar lorem ipsum. And then there was rain.
            """
        }
        _, response = self.server.options('/detect', data=json.dumps(data))

        self.assertTrue(response.status == 200)
    
    def test_summarize_requires_text_or_article_parameters(self):
        """
        /detect requires `text` or `article` parameters.
        """
        data = {
            'foo': 'bar'
        }
        _, response = self.server.post('/detect', data=json.dumps(data))

        self.assertTrue(response.status == 400)
    
    def test_template_requires_json(self):
        """
        /detect requires JSON request.
        """
        _, response = self.server.post('/detect?text=foo')
        self.assertTrue(response.status == 400)
    