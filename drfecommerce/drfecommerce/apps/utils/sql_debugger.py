from django.db.models.query import QuerySet
from pygments import highlight
from pygments.formatters import TerminalFormatter
from pygments.lexers import SqlLexer
from sqlparse import format

class SqlDebugger:
    
    def __init__(self, data=None):
        self.raw_sql = None
        if data:
            self.set_data(data)

    def set_data(self, data):
        if isinstance(data, QuerySet):
            self.raw_sql = str(data.query)
        elif isinstance(data, str):
            self.raw_sql = data
        else:
            raise TypeError("Unsupported data type. Provide a QuerySet or a raw SQL string.")
        
    def pretty_sql(self):
        """Returns a prettified SQL string for the current queryset."""
        if not self.raw_sql:
            print("No SQL set to print.")
            return
        formatted_sql = format(self.raw_sql, reindent=True)
        return highlight(formatted_sql, SqlLexer(), TerminalFormatter())

    def print_sql(self):
        """Prints the prettified SQL to the console."""
        print(self.pretty_sql())