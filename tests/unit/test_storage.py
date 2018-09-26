
"""
Unit tests for the Storage class.
"""
import os
import json
import asyncio
import unittest

from skill.storage import Storage
from datetime import datetime, timedelta


class StorageTestCase(unittest.TestCase):
    """
    Test case for the Storage() class.
    """
    @classmethod
    def setUpClass(cls):
        cls.storage = Storage(os.getenv('POSTGRES_URI'))

    def test_connection_is_managed(self):
        """
        Storage() opens and closes connections correctly.
        """
        with self.storage as S:
            r = S.execute('SELECT TRUE AS connected')[0]['connected']
            self.assertTrue(r)

        self.assertNotEqual(self.storage.connection.closed, 0)
    
    
    def test_pooling_works(self):
        """
        Storage(connection_pool=True) works as expected.
        """
        with Storage(uri=os.getenv('POSTGRES_URI'), pool=True) as S:
            r = S.execute('SELECT TRUE AS connected')[0]['connected']
            self.assertTrue(r)

        self.assertNotEqual(self.storage.connection.closed, 0)
