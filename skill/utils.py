"""
Utility functions for testing different search 
algorithms implemented in this skill.
"""
import signal
import numpy as np

from functools import wraps


class LossFunctions:
    """
    Loss functions to evaluate the performance
    of search algorithms. All methods available in 
    this class take numpy arrays as input.

    Methods
    -------
    mape:
        Mean averaged percentage error.
    rmse:
        Root mean squared error.
    mse:
        Mean squared error.
    """
    @staticmethod
    def mape(A, B):
        """
        Calculates the mean absolute persentage error
        from two series. Original solution from:
        
            https://stats.stackexchange.com/questions/58391/\
                mean-absolute-percentage-error-mape-in-scikit-learn
        
        Parameters
        ----------
        A, B: numpy.array
            Numpy arrays with the same length with the
            two objects representing the results (A)
            and test data (B).

        Returns
        -------
        float
            Floating number in the domain [0, 1].
        """
        #
        #  Let's add 1 to all values
        #  to avoid division by zero.
        #
        A += 0.000000000001
        B += 0.000000000001
        return np.round(np.mean(np.abs(A - B) / A) * 100, 2)

    @staticmethod
    def rmse(A, B):
        """
        Calculates the root mean square error from
        two series. Original solution from:

            https://stackoverflow.com/questions/16774849\
                /mean-squared-error-in-numpy

        Parameters
        ----------
        A, B: numpy.array
            Numpy arrays with the same length with the
            two objects representing the results (A)
            and test data (B).

        Returns
        -------
        float
            Floating number in the same domain
            of the original data.
        """
        return np.round(np.sqrt(np.square(np.subtract(A, B)).mean()), 2)
    
    @staticmethod
    def mse(A, B):
        """
        Calculates the mean square error from
        two series. Original solution from:

            https://stackoverflow.com/questions/16774849\
                /mean-squared-error-in-numpy

        Parameters
        ----------
        A, B: numpy.array
            Numpy arrays with the same length with the
            two objects representing the results (A)
            and test data (B).

        Returns
        -------
        float
            Floating number in the squared domain
            of the original data.
        """
        return np.round(np.square(np.subtract(A, B)).mean(), 2)
