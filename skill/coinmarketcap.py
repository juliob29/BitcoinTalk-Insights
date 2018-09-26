"""
Logic for collecting data directly from the 
CoinMarketCap API.
"""
import requests
import pandas as pd

from memoize import Memoizer
from bs4 import BeautifulSoup
from functools import lru_cache
from datetime import datetime, timedelta

store = {}
cached = Memoizer(store)


class CoinMarketCap:
    """
    Class interface to data from CoinMarketCap. 
    Original data can be found at:

        https://coinmarketcap.com/
    
    """
    def __repr__(self):
        message = """
        Crypto-currency data comes from the website CoinMarketCap.
        CoinMarketCap is can be accessed at: https://coinmarketcap.com/
        The permission to use the data is available on their FAQ

            https://coinmarketcap.com/faq/

        and reads:

            "Q: Am I allowed to use content (screenshots, data, graphs, etc.) 
            for one of my personal projects and/or commercial use?

            R: Absolutely! Feel free to use any content as you see fit. 
            We kindly ask that you cite us as a source."
        
        """
        return message

    def __find_coin(self, coin):
        """
        Maps numberic coin IDs to string slugs and
        vice-versa.

        Parameters
        ----------
        coin: str or int
            Either string or integer that represents
            a coin slug or ID.

        Returns
        -------
        result: dict
            A dictionary with both the coin ID and
            its slug. Example:
                { 'id': 1, 'slug': 'bitcoin' }
        """
        try:
            if isinstance(coin, int):
                match = next((c for c in self.listings() if c['id'] == coin))
            elif isinstance(coin, str):
                match = next((c for c in self.listings() if c['website_slug'] == coin))
        except StopIteration:
            raise ValueError(f'Coin `{coin}` does not exist.')

        result = {
            'id': match['id'],
            'website_slug': match['website_slug']
        }
        return result

    
    @property
    @cached(max_age=60*60*24)
    def status(self):
        """
        Property that retrieves the status of the CoinMarketCap
        API. The status is based on a positive response from
        the /listings endpoint.

        Returns
        -------
        bool:
            Boolean representing the status of the API.
        """
        url = 'https://api.coinmarketcap.com/v2/listings/'
        response = requests.get(url)
        return response.ok

    @property
    @cached(max_age=60*60*24)
    def coin_ids(self):
        """
        Property that represents an interable of 
        coin IDs. These IDs can be used to fetch current
        coin information using the current() method.

        Returns
        -------
        list
            List of strings representing coin IDs.
        """
        return [c['id'] for c in self.listings()]
    
    @property
    @cached(max_age=60*60*24)
    def coin_slugs(self):
        """
        Property that represents an interable of "slugs"
        used as identifiers for the historic() method.
        Example: 'bitcoin' and 'litecoin'

        Returns
        -------
        list
            List of strings representing coin "slugs".

        """
        return [c['website_slug'] for c in self.listings()]

    @classmethod
    @cached(max_age=60*60*5)
    def historic(cls, ticker, 
                 start=(datetime.now() - timedelta(days=90)).strftime('%Y%m%d'), 
                 stop=datetime.now().strftime('%Y%m%d')):
        """
        Retrieves historic data within a time
        period.

        Parameters
        ----------
        ticker: str or int
            Name of ticker to be used (e.g. `bitcoin`)
            or coin ID (e.g. 1).

        start, stop: str
            Start and stop dates in ISO format (YYYY-MM-DD).
            Start's default is now - 90 days.

        Returns
        -------
        list
            List of dictionaries representing the records
            scraped from CoinMarketCap.
        """
        ticker = cls.__find_coin(cls, ticker)

        url = f"https://coinmarketcap.com/currencies/{ticker['website_slug']}/historical-data/?start={start}&end={stop}"
        r = requests.get(url)

        soup = BeautifulSoup(r.content, 'lxml')
        table = soup.find_all('table')[0]
        df = pd.read_html(str(table))[0]

        #
        #  Cleans variables from the original.
        #
        df['Date'] = df['Date'].apply(lambda x: datetime.strptime(x, '%b %d, %Y').strftime('%Y-%m-%d'))
        df['Volume'] = df['Volume'].apply(lambda x: None if x == '-' else x)
        df.columns = ['date', 'open', 'high', 'low', 'close', 'volume', 'market_cap']

        #
        #  Ordering dates in ascending order.
        #
        result = df.sort_values('date').to_dict(orient='records')

        return result

    @classmethod
    @cached(max_age=60*60*24)
    def listings(cls, limit=None):
        """
        Returns a full list of available coins alongside their
        names and IDs.

        Parameters
        ----------
        limit: int, default None
            Limit the output to the top N coins. This
            is only useful when experimenting and when 
            the user doesn't want all coins returned at once.

        Response
        --------
        List with all available coin information.
        """
        url = 'https://api.coinmarketcap.com/v2/listings/'
        response = requests.get(url)

        return response.json()['data']

    @classmethod
    @cached(max_age=60*60*24)
    def current(cls, ticker):
        """
        Fetches current prices from CoinMarketCap.

        Returns
        -------
        Dictionary with a single record form the 
        """
        ticker = cls.__find_coin(cls, ticker)
        url = f"https://api.coinmarketcap.com/v2/ticker/{ticker['id']}/"

        response = requests.get(url)

        return response.json()
