# database_manager.py

import mysql.connector
from mysql.connector import errorcode


class DatabaseManager:
    """Manages the connection to a MySQL database."""

    def __init__(self):
        """Initializer."""
        self.connection = None
        self.cursor = None

    # In database_manager.py

    def connect(self, db_config):
        """
        Establishes a connection to the database.

        Args:
            db_config (dict): A dictionary with connection details.

        Returns:
            bool: True if connection is successful, False otherwise.
        """
        try:
            # Create a copy so we don't modify the original dict
            config = db_config.copy()

            # The mysql.connector.connect function doesn't like a 'database' key
            # with a value of None or an empty string. So, we remove it if it's falsy.
            if not config.get("database"):
                config.pop("database", None)

            self.connection = mysql.connector.connect(**config)
            self.cursor = self.connection.cursor()
            print("Database connection successful.")
            return True
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                print("Error: Something is wrong with your user name or password")
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                print("Error: Database does not exist")
            else:
                print(f"An unexpected error occurred: {err}")
            return False

    def disconnect(self):
        """Closes the database connection."""
        if self.connection and self.connection.is_connected():
            self.cursor.close()
            self.connection.close()
            print("Database connection closed.")

    def list_tables(self):
        """
        Retrieves a list of tables from the connected database.

        Returns:
            list: A list of table names, or an empty list if an error occurs
                  or if not connected.
        """
        if not (self.connection and self.connection.is_connected()):
            print("Not connected to a database.")
            return []

        try:
            self.cursor.execute("SHOW TABLES;")
            tables = [table[0] for table in self.cursor.fetchall()]
            return tables
        except mysql.connector.Error as err:
            print(f"Failed to list tables: {err}")
            return []
