from intake.source import base
from . import __version__

class SQLTable(base.DataSource):
    """
    Docstring goes here!

    Parameters
    ----------
    uri: str or None
        Full connection string in sqlalchemy syntax
    sql_table: str
        Query expression to pass to the DB backend
    sql_kwargs: dict
        Further arguments to pass to pandas.read_sql
    """
    name = 'sql_table'
    version = __version__
    container = 'dataframe'
    partition_access = True

    def __init__(self, uri, sql_table, sql_kwargs={}, metadata={}):
        self._init_args = {
            'uri': uri,
            'sql_table': sql_table,
            'sql_kwargs': sql_kwargs,
            'metadata': metadata,
        }

        self._uri = uri
        self._sql_table = sql_table
        self._sql_kwargs = sql_kwargs
        self._dataframe = None

        super(SQLTable, self).__init__(metadata=metadata)


    def read(self):
        return "Hello World"