"""
Interface for retrieving scraped data
from bitcointalk.org
"""
import os
import psycopg2
import datetime

from isoweek import Week
from memoize import Memoizer
from sanic.log import logger
from skill.storage import Storage

store = {}
cached = Memoizer(store)

class BitcoinTalk:
    """
    Class that provides an interface for getting
    scraped bitcointalk.org data from the database.
    The forum data is downloaded using the 
    `skill-scraper`.

    """

    def __init__(self):

        self.uri = os.getenv('POSTGRES_URI')
        self.monday_last_week = str((Week.thisweek() - 1).monday())
        self.sunday_last_week = str((Week.thisweek() - 1).sunday())

    def __start_to_end_date(self, start, stop):
        """
        Fetches all BitcoinTalk data from within
        a specified time period.
        
        Parameters
        ----------
        start, stop: str
            Date strings in ISO format.

        Returns
        -------
        result: list
            List of messages from database.
        """
        with Storage(self.uri) as S:
            sql = f"""
                SELECT 
                    subject,
                    content_no_quote_no_html 
                FROM message 
                WHERE post_time > '{start}' AND 
                      post_time <= '{stop}'
            """
            result = S.execute(sql)

        return result

    def last_week(self):
        """
        Fetches last week's data from the database.
        A week is defined as seven days prior to current day.

        Returns
        -------
        list
            List of records from database.
        """
        return self.__start_to_end_date(self.monday_last_week,
                                        self.sunday_last_week)

    def all(self):
        """
        Fetches all records from database.
        
        Returns
        -------
        result: list
            Records from database.
        """
        with Storage(self.uri) as S:
            result = S.execute("SELECT * FROM message")

        return result

    def sample(self, sample_size=0.01):
        """
        Get a random sample from the database using PostgreSQL's
        random sampling features (SYSTEM method). Refer to
        official PostgreSQL documentation here:

            * https://www.postgresql.org/docs/9.6/static/tablesample-method.html

        Parameters
        ----------
        sample_size: float
            Share of records to return. 
        
        Returns
        -------
        result: list
            Results from database.

        """
        with Storage(self.uri) as S:
            sql = f"""
            SELECT
                subject,
                link,
                content_no_quote_no_html
            FROM message
            TABLESAMPLE SYSTEM('{sample_size}')
            """
            result = S.execute(sql)

        return result

    @cached(max_age=60 * 60 * 12)
    def latest_message(self,coin):
        if isinstance(coin,list):
            logger.info("Input is list!")
            results = []
            S = Storage(self.uri)
            S.open()
            for c in coin:
                logger.info(f"Querying for {c}")
                sql = f"""
                    SELECT
                        link
                    FROM message
                    WHERE to_tsvector('english', content_no_quote_no_html) @@ to_tsquery('english', '{c}')
                        ORDER BY post_time DESC
                        LIMIT 1
                    """
                results.append(S.execute(sql)[0]['link'])
                logger.info(f"Querying for {c} complete!")
            S.close()
            return results
        
        else:
            with Storage(self.uri) as S:
                sql = f"""
                    SELECT
                        link
                    FROM message
                    WHERE to_tsvector('english', content_no_quote_no_html) @@ to_tsquery('english', '{coin}')
                        ORDER BY post_time DESC
                        LIMIT 1
                    """
                result = S.execute(sql)

            return result[0]['link']
