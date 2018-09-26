import os 
import psycopg2 as postgres
import psycopg2.extras

from psycopg2.pool import SimpleConnectionPool


class Storage:
    """
    Storage class; provides interface to all 
    BitcoinTalk storage methods. Only PostgreSQL
    is currently supported via this method. 
    More methods may be supported in the future.
    Parameters
    ----------
    uri: str
        PostgreSQL connection string.
    """

    def __init__(self, uri, pool=False):
        self.uri = os.getenv('POSTGRES_URI')
        self.pool = pool

        if self.pool:
            self.connection_pool = SimpleConnectionPool(10, 10**2, self.uri)
    

    def __enter__(self):
        self.open()
        return self

    def __exit__(self, exception_type, exception_value, traceback):
        self.close()

    def open(self):
        """
        Opens connection to PostgreSQL instance.
        Returns
        -------
        A psycopg2 cursor.
        """
        if self.pool:
            self.connection = self.connection_pool.getconn()
        else:
            self.connection = postgres.connect(self.uri)

        self.connection.autocommit = True
        self.cursor = self.connection.cursor(
            cursor_factory=psycopg2.extras.RealDictCursor)

        return self.cursor

    def close(self):
        """
        Closes connection to PostgreSQL instance.
        Returns
        -------
        Response from closing the connection to 
        the database.
        """
        self.cursor.close()
        if self.pool:
            self.connection_pool.closeall()
            r = True
        else:
            r = self.connection.close()
        return r

    def execute(self, sql, values=None):
        """
        Executes artibrary SQL snippet.
        Parameters
        ----------
        sql: str
            SQL snippet to execute.
        
        values: list, default None
            Values to replace the string with.
            These values use psycopg2's string
            formatting functions to avoid
            programming errors.
        
        Returns
        -------
        Dictionary with responses query
        responses from psycopg2.
        """
        if values:
            self.cursor.execute(sql, values)
        else:
            self.cursor.execute(sql)

        row_count_methods = ['DELETE', 'INSERT', 'UPDATE']
        if any(m in sql for m in row_count_methods):
            result = self.cursor.rowcount
        else:
            result = []
            for row in self.cursor:
                result.append(row)

        return result