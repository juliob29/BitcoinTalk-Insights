"""
Skill can find cryptocurrencies in text, and give their current listings.
"""
import re
import os
import time 
import gensim
import schedule
import plotly
import plotly.plotly as py

from isoweek import Week
from sanic.log import logger
from memoize import Memoizer
from nltk.corpus import wordnet as wn
from datetime import datetime, timedelta
from skill.bitcointalk import BitcoinTalk
from skill.coinmarketcap import CoinMarketCap

store = {}
cached = Memoizer(store)


class Crypto:
    """
    This classes uses the CoinMarketCap library, along with a 
    regex search, to search for cryptocurrencies in a body
    of text, and output its current listing price in 
    the overall market.

    Parameters
    ----------
    model_path: str, default None
        Location of model to load. If left as None,
        this class will attempt to load the latest
        available model.

    related: bool, default False
        If the class should load the word2vec model
        for computing similarity statistics between
        currencies.

    ing_backend: str, default 'plotly'
        The charting backend to instantiate the Chart()chart
        class with. It can be either 'plotly' or 'image'

    """

    def __init__(self, model_path=None):


        self.__initialize_variables()

    def model_setting(self, model_path=None,original=True):
        
        
        self.full_trained = 'models/trained.model'
    

        #
        #  If the user passes no model path,
        #  then simply try to get the model from
        #  the latest week available.
        #
        last_week = str(Week.thisweek() - 1)
        directory = os.getenv('MODELS_PATH')
        if not model_path:
            self.model_path = os.path.join(directory, last_week + '.model')
        else:
            self.model_path = model_path
        

        try:
            self.model = gensim.models.Word2Vec.load(self.model_path)
        except FileNotFoundError:
            self.model = gensim.models.Word2Vec.load(self.full_trained)
            self.model_path = self.full_trained

        self.comparison_results = self.coin_comparison()

        if original == True:
            self.previous_model = self.model
        else: 
            pass 

        return self.model, self.model_path, self.comparison_results


    def __initialize_variables(self):
        """
        Restricts currencies to only currencies without a definition in WordNet.
        Returns
        -------
        self.currencies,self.symbols,self.website_slugs
            These variables contain the name, symbols, and website_slugs.
        """


        coins = CoinMarketCap.listings()
        currencies = [currency['name'] for currency in coins]
        # symbols = [currency['symbol']for currency in coins]
        coin_removal = []
        undesirable_coins = ['Crypto', 'ICOS', 'Naviaddress', 'B2BX']

        for i, currency in enumerate(currencies):
            if wn.synsets(currency) or currency in undesirable_coins:
                coin_removal.append(i)

        for index in sorted(coin_removal, reverse=True):
            del coins[index]

        self.coins = coins
        self.currencies = [currency['name'] for currency in coins]
        self.symbols = [currency['symbol'] for currency in coins]
        self.website_slugs = [currency['website_slug'] for currency in coins]
        self.coin_market_cap = CoinMarketCap()
        self.BitcoinTalk = BitcoinTalk()
        self.model_setting()

    def _collect_coin_data(self,
                            coin,
                            start=(datetime.now() - timedelta(days=90)).strftime('%Y%m%d'),
                            dates_as_strings=True):
        """
        Simple method for collecting cryptocurrency data
        using CoinMarketCap().historic() and for parsing
        that data into the format expected by the
        Chart() class.
        Parameters
        ----------
        coin: str
            ID that identifies a unique cryptocurrency in
            CoinMarketCap.
        start: str, default datetime.now() - timedelta(days=90)
            String with a date value with ISO formatting.
        Returns
        -------
        plot_data: dict
            Dictionary with two keys: `date` and `close`.
            These keys contain lists of the dates and
            values for each cryptocurrency.
        """
        series = self.coin_market_cap.historic(coin, start=start)
        plot_data = {'date': [], 'close': []}
        for record in series:

            if dates_as_strings:
                date = record['date']
            else:
                date = datetime.strptime(record['date'], '%Y-%m-%d')

            plot_data['date'].append(date)
            plot_data['close'].append(record['close'])

        return plot_data

    @cached(max_age=60 * 60 * 10)
    def regex_crypto_currency_finder(self, string):
        '''
        This uses a regex to find a given currency, and place it in a list. 
        The list then places its results in the results dictionary. 
        This is done for regular currencies, its plurals, and its' symbols.
        Parameters
        ----------
        text: str
            Textual content to summarize.
        Returns
        -------
        result: Array of Objects
            Contains currency detected, its location, and the original sentence.
        '''

        results = []
        matches = {}
        caught_coin = []
        logger.info('Running regex on input')

        for i, currency in enumerate(self.currencies):
            regex = r"\b{}\b".format(currency)
            pattern = list(re.finditer(regex, string, re.I | re.M))

            count = 0
            # SINGULAR
            for match in pattern:
                if count == 0:
                    results.append({
                        "sentence": string,
                        "cryptocurrency": self.website_slugs[i],
                        "name": self.currencies[i],
                        "findings": [{
                            "name_start": match.start(),
                            "name_end": match.end()
                        }]
                    })
                    count = count + 1
                else:
                    matches.update({'name_start': match.start()})
                    matches.update({'name_end': match.end()})
                    for result in results:
                        if result['name'] == self.currencies[i]:
                            result['findings'].append(matches)
                        else:
                            pass
                    matches = {}

            regex_plural = r"\b{}s\b".format(currency)
            pattern_plural = list(
                re.finditer(regex_plural, string, re.I | re.M))

            #PLURAL
            for match in pattern_plural:
                if count == 0:
                    results.append({
                        "sentence": string,
                        "cryptocurrency": self.website_slugs[i],
                        "name": self.currencies[i],
                        "findings": [{
                            "name_start": match.start(),
                            "name_end": match.end()
                        }]
                    })
                    count = count + 1
                else:
                    matches.update({'name_start': match.start()})
                    matches.update({'name_end': match.end()})
                    for result in results:
                        if result['name'] == self.currencies[i]:
                            result['findings'].append(matches)
                        else:
                            pass
                    matches = {}

            if count > 0:
                caught_coin.append(i)
            else:
                pass
            count = 0

        count = 0
        #SYMBOL

        for i, symbol in enumerate(self.symbols):
            regex_symbol = r"\b{}\b".format(symbol)
            pattern_symbol = list(re.finditer(regex_symbol, string))

            for match in pattern_symbol:
                if count == 0 and i not in caught_coin:
                    results.append({
                        "sentence": string,
                        "cryptocurrency": self.website_slugs[i],
                        "name": self.currencies[i],
                        "findings": [{
                            "symbol_start": match.start(),
                            "symbol_end": match.end()
                        }]
                    })
                    count = count + 1
                elif i in caught_coin:
                    matches.update({'name_start': match.start()})
                    matches.update({'name_end': match.end()})

                    for result in results:
                        if result['name'] == self.currencies[i]:
                            result['findings'].append(matches)
                        else:
                            pass
                    matches = {}
            count = 0

        if not results:
            logger.info(
                'Did not find cryptocurrency in input. Returning empty.')
        else:
            logger.info(
                'Found {} cryptocurrencie(s). Limiting.'.
                format(len(results)))

        return results

    @cached(max_age=60*60*10)
    def text(self, text, limit):
        """
        Uses text as an input. Regex search is called on text in order to return
        information about found cryptocurrencies
        Parameters
        ----------
        text: str
            Textual content to search for cryptocurrencies.
        limit: int 
            Limits regex output to value of int. Currencies with the most finds
            are the ones returned.
        Returns
        -------
        result: Array of Objects
            Contains currency detected, its location, its current close price,
            and a link to a plotly graph.
        """

        logger.info('Running skill. Input size: {} characters'.format(len(text)))

        findings = self.regex_crypto_currency_finder(text)

        sorted_findings = sorted(
            [{
                'coin': d['cryptocurrency'],
                'n': len(d['findings'])
            } for d in findings],
            key=lambda x: x['n'],
            reverse=True)
        top_coins = [x['coin'] for x in sorted_findings[:limit]]

        top_findings = [
            d for d in findings if d['cryptocurrency'] in top_coins
        ]

        results = []

        logger.info(f'The length of the findings is: {len(top_findings)}')

        for finding in top_findings:
            related = []

            try:
                logger.info(f"Starting related calculation for {finding['name']}")

                related = self.comparison_results[finding['name'].lower()][:5]

                logger.info(f"Finished related calculation for {finding['name']}")
                logger.info(f"Starting URL fetching for {finding['name']} related coins")

                name_of_related = []
                for coin in related:
                    name_of_related.append(coin['name'])
                
                logger.info(name_of_related)
                logger.info(type(name_of_related))

                all_links = self.BitcoinTalk.latest_message(name_of_related)

                for i,coin in enumerate(related): 
                    coin['url'] = all_links[i]

                logger.info(f"Finished URL fetching for {finding['name']} related coins")
                
            except KeyError:
                related = []

            except AttributeError:
                coin['url'] = None
            
            results.append({
                'title': f"See the latest conversation about {finding['name']} on bitcointalk.org",
                'entities':[
                    {
                    "name": finding['name'],
                    'start': 34,
                    'end': 34 + len(finding['name']),
                    'url': self.BitcoinTalk.latest_message(finding['name']),
                    'related': related
                    }
                ]
            })
            logger.info(f"Finished JSON for {finding['name']}")

        return results

    def coin_comparison(self):
        """
        Compares all coins in currencies to other coins based on Word2Vec similarity.
        Returns
        -------
        similar_results: Dictionary.
            Contains a dictionary with cryptocurrencies as keys, and a list of
            dictionaries as its values, showing from greatest to least, 
            the related currencies to the key.
        
        """
        logger.info(f'Running related coins with {self.model_path}')
        similar_results = {}
        new_list = []
        lower_currencies = []
        count = 0

        for currency in self.currencies:
            lower_currencies.append(currency.lower())

        for currency in lower_currencies:
            coin_dict = []
            for cc in lower_currencies:
                try:
                    model_similarity = self.model.wv.similarity(currency, cc)
                    name = [
                        x['name'] for x in self.coins
                        if x['name'].lower() == cc
                    ][0]
                    slug = [
                        x['website_slug'] for x in self.coins
                        if x['name'].lower() == cc
                    ][0]

                    coin_dict.append({
                        "name": name,
                        "slug": slug,
                        "value": model_similarity,
                        "url": ""
                    })

                except (KeyError, IndexError):
                    pass

            if coin_dict:
                similar_results.update({currency: coin_dict})
            else:
                pass

        for key, value in similar_results.items():
            new_list.append(
                sorted(value, key=lambda x: x['value'], reverse=True))
            similar_results.update({key: new_list[count]})
            count = count + 1

        for value in similar_results.values():
            del (value[0])

        logger.info('Related coins saved.')
        return similar_results