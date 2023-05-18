import pymysql.cursors
from database.config import HOSTNAME, USERNAME, PASSWORD, DATABASE


class DatabaseConnector:
    """
        Manages the connection to a database.
    """
    __instance = None

    def __new__(cls, *args, **kwargs):
        """
        Create and return a new instance of the DatabaseConnector class,
        or return an existing instance if one already exists.
        """
        if cls.__instance is None:
            cls.__instance = super(DatabaseConnector, cls).__new__(cls)
        return cls.__instance

    def __init__(self):
        """
        Initialize the DatabaseConnector instance.
        """
        self.connection = None

    def connect(self):
        """
        Connect to the database and return the connection.

        Returns:
            pymysql.Connection: The database connection.
        """
        try:
            self.connection = pymysql.connect(
                host=HOSTNAME,
                port=3306,
                user=USERNAME,
                password=PASSWORD,
                database=DATABASE,
                cursorclass=pymysql.cursors.DictCursor,
            )
            return self.connection
        except pymysql.Error as ex:
            print("Failed connection with database")
            print(ex)

    def close(self):
        """
        Close the database connection.
        """
        if self.connection:
            self.connection.close()
