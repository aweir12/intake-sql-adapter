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

    def _load(self):
        import pandas as pd
        sql_query = "select top 100 * from {}".format(self._sql_table)
        loader = pd.read_sql
        self._dataframe = loader(sql_query, self._uri, **self._sql_kwargs)
    
    def _get_schema(self):
        if self._dataframe is None:
            self._load()
        return base.Schema(datashape=None,
                           dtype={idx : str(val) for idx, val in self._dataframe.dtypes.items()},
                           shape=self._dataframe.shape,
                           npartitions=1,
                           extra_metadata={})

    def _get_partition(self, _):
        if self._dataframe is None:
            self._load_metadata()
        return self._dataframe

    def read(self):
        return self._get_partition(None)