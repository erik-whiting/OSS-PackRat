import datetime
from distutils.log import error
import psycopg2
import psycopg2.extras
import os

user = os.getenv("DB_USER")
password = os.getenv("DB_PASSWORD")
host = os.getenv("DB_HOST")
port = os.getenv('DB_PORT', "5432")


class Connection:
    """
    This is the main database connection class.

    As of right now, OSS PackRat only supports Postgres
    RDBMS. Also, the project does not use a 3rd party
    ORM because at the time of development, that seemed
    like overkill, and rolling our own ORM works fine
    for our purposes.
    """

    def __init__(self, db_name: str = "OSSPackRat", error_log="db_error_log.csv"):
        """
        Constructs an instance of the connection class. This class
        assumes that you have already created a database called
        OSSPackRat. If you named your database something else, all
        you have to do is pass the name to the constructor as a
        string. This class also assumes you want to log all your
        errors to a CSV file called db_error_log.csv at the project
        root level.

        Please note, this class assumes that you have the following
        environment variables set:

        DB_USER       : The user of your postgres instance
        DB_PASSWORD   : The postgres user's password
        DB_HOST       : The host name of your database

        If these are not set, no connection will be established.

        Parameters
        ----------
        db_name : str, OSSPackRat
          The name of the database you're using. The default
          value is OSSPackRat, so if you've named the database
          something else, just pass that name as a string to
          the constructor.

        error_log : str, db_error_log.csv

        Examples
        --------
        # For databases named OSSPackRat
        connection = Connection()
        # For databases named something else
        connection = Connection("database_name")
        # For a test database with test error log
        connection = Conection("osspackrat_test", "test_db_error_log.csv")

        """
        self.con = psycopg2.connect(
            database=db_name, user=user, password=password, host=host, port=port
        )
        self.error_log = error_log

    def close(self) -> None:
        """
        This function is a wrapper for the database
        connection object's `close` method.
        """
        self.con.close()


class Query:
    """
    This class serves as the only interface to the database. It
    was decided that this project's size and scope did not merit
    the use of a 3rd party ORM, so we rolled our own. This class
    contains the core functionality of our ORM.
    """

    def __init__(self, connection: Connection):
        """
        Returns an instance of the `Query` class. This class provides
        the only database interface for the entire project. You must
        instantiate this class with a `Connection` object.

        Parameters
        ----------
        connection : Connection

        Examples
        --------
        # For databases named OSSPackRat
        connection = Connection()
        q = Query(connection)
        # For databases named something else
        connection = Connection("database_name")
        q = Query(connection)
        """
        self.connection = connection
        self.cursor = self.connection.con.cursor(
            cursor_factory=psycopg2.extras.DictCursor
        )
        self.error_log = self.connection.error_log

    def execute(self, sql: str) -> None:
        """
        As its name suggests, this method simply executes the
        SQL string passed to it. It's not meant to be invoked
        directly, but it's also not a private method in case
        someone needs to execute some DDL statements. Outside of
        this class, you most likely the `command` method instead
        of this one.

        Parameters
        ----------
        sql : str
          The SQL command to execute

        Examples
        --------
        # Assume the variable `q` is an instance of `Query`
        sql = "INSERT INTO table (c1, c2) VALUES (v1, v2);"
        q.execute(sql)
        """
        try:
            self.cursor.execute(sql)
        except Exception as e:
            self.log_error(sql, e)

    def command(self, sql: str) -> None:
        """
        This method is inteded to be used for SQL commands that
        don't return a result. This method is mostly intended
        for INSERTS and UPDATES. However, this method exists
        here as a helper to the `insert` and `update` methods
        of this class. Again, you most likely don't need it.

        Parameters
        ----------
        sql : str
          The SQL command to execute

        Examples
        --------
        # Assume the variable `q` is an instance of `Query`
        sql = "INSERT INTO table (c1, c2) VALUES (v1, v2);"
        q.command(sql)
        """
        self.cursor.execute(sql)
        try:
            self.connection.con.commit()
        except Exception as e:
            self.log_error(sql, e)

    def query(self, sql: str) -> list[str]:
        """
        The `query` method is the primary means of getting
        data out of the database. Simply pass it a SQL string
        and expect the results to be returned in a `list`. This
        method implements the `execute` method, and then uses
        the class `cursor` attribute to grab results.
        """
        self.execute(sql)
        results = []
        for row in self.cursor.fetchall():
            results.append(row)
        return results

    def log_error(self, sql, exception=""):
        """
        The `log_error` method supports reproducibility by
        keeping track of any database actions that fail. This
        makes data gathering and analysis transparent and
        allows both researchers and reviewers to understand
        the full picture of the data generated. Database
        errors are saved to `db_error_log.csv` in the project
        root. It contains the data, the erring SQL, and the
        exception message.
        """
        print("Something went wrong, logging error")
        now = datetime.datetime.now().strftime("%D %H:%M:%S")
        f = open(self.error_log, "a+")
        f.write(f"{now}, {sql}, {exception}")
        f.close()
