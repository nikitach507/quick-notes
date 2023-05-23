from database.connect_database import DatabaseConnector
from lib_imports import Optional


class CategoryDatabaseAction:
    """
    Provides methods for managing categories in a database.
    """

    def __init__(self):
        """
        Initialize a CategoryDatabaseAction instance.
        """
        pass

    @staticmethod
    def _execute_query(query: str, params: Optional[tuple] = None):
        """
        Execute the specified query with optional parameters.

        Args:
            query (str): The SQL query to execute.
            params (tuple, optional): The parameters to substitute in the query.
            Defaults to None.
        """
        db_connector = DatabaseConnector()
        connection = db_connector.connect()
        try:
            with connection.cursor() as cursor:
                if params:
                    cursor.execute(query, params)
                else:
                    cursor.execute(query)
                connection.commit()
        finally:
            db_connector.close()

    def add_category(self, table_name: str, name_cat: str):
        """
        Add a category to the specified table.

        Args:
            table_name (str): The name of the table to add the category to.
            name_cat (str): The name of the category.
        """
        insert_query = "INSERT INTO `%s` (name_cat) VALUES (%%s);" % table_name
        params = (name_cat,)
        self._execute_query(insert_query, params)
        print("Adding a category was successful")
        print("#" * 20)

    @staticmethod
    def edit_category(table_name: str, name_cat_now: str, name_cat_after: str):
        """
        Edit a category in the specified table.

        Args:
            table_name (str): The name of the table containing the category.
            name_cat_now (str): The current name of the category.
            name_cat_after (str): The new name of the category.
        """
        update_query = (
                "UPDATE `%s` SET name_cat = %%s WHERE name_cat = %%s;" % table_name
        )
        params = (name_cat_after, name_cat_now)
        CategoryDatabaseAction._execute_query(update_query, params)
        print("Editing the category was successful")
        print("#" * 20)

    @staticmethod
    def delete_category(table_name: str, name_cat_now: str):
        """
        Delete a category from the specified table.

        Args:
            table_name (str): The name of the table containing the category.
            name_cat_now (str): The name of the category to delete.
        """
        delete_query = "DELETE FROM `%s` WHERE name_cat = %%s;" % table_name
        params = (name_cat_now,)
        CategoryDatabaseAction._execute_query(delete_query, params)
        print("Deleting the category was successful")
        print("#" * 20)

    @staticmethod
    def delete_all_categories(table_name: str):
        """
        Delete all categories from the specified table.

        Args:
            table_name (str): The name of the table containing the categories.
        """
        delete_all_rows = "DELETE FROM `%s`;" % table_name
        CategoryDatabaseAction._execute_query(delete_all_rows)
        print("Deletion of all categories was successful")
        print("#" * 20)

    @staticmethod
    def select_all_categories(table_name: str):
        """
        Retrieve and print all categories from the specified table.

        Args:
            table_name (str): The name of the table containing the categories.
        """
        db_connector = DatabaseConnector()
        connection = db_connector.connect()
        try:
            with connection.cursor() as cursor:
                select_all_rows = "SELECT name_cat FROM `%s`;" % table_name
                cursor.execute(select_all_rows)

                rows = cursor.fetchall()
                for row in rows:
                    print(row)
                print("#" * 20)
        finally:
            db_connector.close()

    @staticmethod
    def all_categories_list(table_name: str):
        """
        Retrieve a list of all categories from the specified table.

        Args:
            table_name (str): The name of the table containing the categories.

        Returns:
            list: A list of all categories.
        """
        db_connector = DatabaseConnector()
        connection = db_connector.connect()
        try:
            with connection.cursor() as cursor:
                select_all_rows = "SELECT name_cat FROM `%s`;" % table_name
                cursor.execute(select_all_rows)

                rows = cursor.fetchall()
                all_cat_list = [row["name_cat"] for row in rows]
                return all_cat_list
        finally:
            db_connector.close()
