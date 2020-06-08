from intake.source import base
from . import __version__

class SQLTest():
    name = 'sql'
    version = __version__

    def __init__(self, uri):
        self.first_name = uri