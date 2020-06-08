from intake.source import base
from . import __version__

class SQLTable(base.DataSource):
    """
    One-shot SQL to dataframe reader (no partitioning)
    Caches entire dataframe in memory.
    Parameters
    ----------
    uri: str or None
        Full connection string in sqlalchemy syntax
    sql_expr: str
        Query expression to pass to the DB backend
    sql_kwargs: dict
        Further arguments to pass to pandas.read_sql
    """
    name = 'sql_table'
    version = __version__
    container = 'dataframe'
    partition_access = True

    def __init__(self, uri, sql_expr, sql_kwargs={}, metadata={}):
        self._init_args = {
            'uri': uri,
            'sql_expr': sql_expr,
            'sql_kwargs': sql_kwargs,
            'metadata': metadata,
        }

        self._uri = uri
        self._sql_expr = sql_expr
        self._sql_kwargs = sql_kwargs
        self._dataframe = None

        super(SQLTable, self).__init__(metadata=metadata)

    def _load(self):
        import pandas as pd
        loader = pd.read_sql
        self._dataframe = loader(self._sql_expr, self._uri, **self._sql_kwargs)

    def _get_schema(self):
        if self._dataframe is None:
            self._load()
        return base.Schema(datashape=None,
                           dtype=self._dataframe.dtypes,
                           shape=self._dataframe.shape,
                           npartitions=1,
                           extra_metadata={})

    def _get_partition(self, _):
        if self._dataframe is None:
            self._load_metadata()
        return self._dataframe

    def read(self):
        return self._get_partition(None)

    def _close(self):
        self._dataframe = None