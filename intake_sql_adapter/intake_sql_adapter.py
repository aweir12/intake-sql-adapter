from intake.source import base
from . import __version__

class SQLTable(base.DataSource):
    """
    Class to query a single SQL table or view.

    Parameters
    ----------
    uri: str or None
        Full connection string in sqlalchemy syntax
    sql_table: str
        Table or view to query
    sql_num_rows: int
        Number of rows to return from sql query
    sql_where_clause: str
        where clause of SQL statement to be passed
    sql_kwargs: dict
        Further arguments to pass to pandas.read_sql
    """
    name = 'sql_table'
    version = __version__
    container = 'dataframe'
    partition_access = True

    def __init__(self, uri, sql_table, sql_num_rows = 100, sql_where_clause = "1=1", sql_kwargs={}, metadata={}):
        self._init_args = {
            'uri': uri,
            'sql_table': sql_table,
            'sql_num_rows': sql_num_rows,
            'sql_where_clause' : sql_where_clause,
            'sql_kwargs': sql_kwargs,
            'metadata': metadata,
        }

        self._uri = uri
        self._sql_table = sql_table
        self._sql_expr = "select top {} * from {} where {}".format(sql_num_rows, sql_table, sql_where_clause)
        self._sql_num_rows = sql_num_rows
        self._sql_where_clause = sql_where_clause
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

    def _close(self):
        self._dataframe = None