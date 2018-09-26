"""
Tests for the LossFunction class.
"""
import unittest
import numpy as np

from skill.utils import LossFunctions


class LossFunctionsTestCase(unittest.TestCase):
    """
    Test case for the LossFunctions() class.
    """
    def test_mape_returns_correct_numbers(self):
        """
        LossFunctions.mape() returns correct fraction.
        """
        A = np.array(list(range(1, 11)), dtype='float64')
        B = A * 1.1
        result = LossFunctions.mape(A, B)

        self.assertAlmostEqual(result, 10)
    
    def test_rmse_returns_correct_numbers(self):
        """
        LossFunctions.rmse() returns correct fraction.
        """
        A = np.array(list(range(1, 11)), dtype='float64')
        B = A * 1.1
        result = LossFunctions.rmse(A, B)

        self.assertAlmostEqual(result, 0.62)
    
    def test_mse_returns_correct_numbers(self):
        """
        LossFunctions.mse() returns correct fraction.
        """
        A = np.array(list(range(1, 11)), dtype='float64')
        B = A * 1.1
        result = LossFunctions.mse(A, B)

        self.assertAlmostEqual(result, 0.39)
