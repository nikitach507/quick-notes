from lib_imports import Optional, Literal
from database.connect_database import DatabaseConnector


class NotesDatabaseAction:
    """
        Provides actions for managing notes in a database.
    """

    def __init__(self, note_name: str, note_description: str, note_category: str):
        """
        Initializes a NotesDatabaseAction instance.

        Args:
            note_name (str): The name of the note.
            note_description (str): The description of the note.
            note_category (str): The category of the note.
        """
        self.note_name = note_name
        self.note_description = note_description
        self.note_category = note_category

    @staticmethod
    def _execute_query(query: str, params: Optional[tuple] = None):
        """
        Executes a database query with optional parameters.

        Args:
            query (str): The SQL query to execute.
            params (tuple, optional): The parameters to be used in the query. Defaults to None.
        """
        db_connector = DatabaseConnector()
        connection = db_connector.connect("notes")
        try:
            with connection.cursor() as cursor:
                if params:
                    cursor.execute(query, params)
                else:
                    cursor.execute(query)
                connection.commit()
        finally:
            db_connector.close()

    def add_note(self, table_name: str, user_id):
        """
        Adds a note to the specified table in the database.

        Args:
            table_name (str): The name of the table to add the note to.
        """
        insert_query = (
                "INSERT INTO `%s` (user_id, note_name, note_description, note_category) "
                "VALUES (%%s, %%s, %%s, %%s);"
                % table_name
        )
        params = (user_id, self.note_name, self.note_description, self.note_category)
        self._execute_query(insert_query, params)
        print("Adding a note was successful")
        print("#" * 20)

    def edit_note(
            self,
            table_name: str,
            user_id,
            note_id: int,
            new_name: Optional[str] = None,
            new_desc: Optional[str] = None,
            new_category: Optional[str] = None
    ):
        """
        Edits a note in the specified table in the database.

        Args:
            table_name (str): The name of the table containing the note.
            note_id (int): The ID of the note to edit.
            new_name (str, optional): The new name for the note. Defaults to None.
            new_desc (str, optional): The new description for the note. Defaults to None.
            new_category (str, optional): The new category for the note. Defaults to None.
        """
        if new_name is None:
            new_name = self.note_name
        if new_desc is None:
            new_desc = self.note_description
        if new_category is None:
            new_category = self.note_category
        update_query = (
                "UPDATE `%s` SET note_name = %%s, note_description = %%s, note_category = %%s "
                "WHERE user_id = %%s AND id = %%s;"
                % table_name
        )
        params = (new_name, new_desc, new_category, user_id, note_id)
        self._execute_query(update_query, params)
        print("Editing the note was successful")
        print("#" * 20)

    @staticmethod
    def edit_category_in_note(table_name: str, user_id, name_cat_now: str, name_cat_after: str):
        edit_query = "UPDATE `%s` SET note_category = %%s WHERE user_id = %%s AND note_category = %%s;" % table_name
        params = (name_cat_after, user_id, name_cat_now)
        NotesDatabaseAction._execute_query(edit_query, params)
        print("Editing the note was successful")
        print("#" * 20)

    @staticmethod
    def delete_note(table_name: str, user_id, note_id: int):
        """
        Deletes a note from the specified table in the database.

        Args:
            table_name (str): The name of the table containing the note.
            note_id (int): The ID of the note to delete.
        """
        delete_query = "DELETE FROM `%s` WHERE user_id = %%s AND id = %%s;" % table_name
        params = (user_id, note_id)
        NotesDatabaseAction._execute_query(delete_query, params)
        print("Deleting the note was successful")
        print("#" * 20)

    @staticmethod
    def delete_all_note_in_category(table_name: str, user_id, name_cat_to_delete: str):
        delete_query = "DELETE FROM `%s` WHERE user_id = %%s AND note_category = %%s;" % table_name
        params = (user_id, name_cat_to_delete)
        NotesDatabaseAction._execute_query(delete_query, params)
        print(f"Deleting the all note from the category '{name_cat_to_delete}' was successful")
        print("#" * 20)

    @staticmethod
    def select_all_notes(
            table_name: str, user_id, category: str,
            sorting: Literal["newest", "oldest", "atoz", "ztoa"]
    ):
        """
        Retrieves all notes from the specified table in the database,
        filtered by category and sorted according to the specified sorting option.

        Args:
            table_name (str): The name of the table containing the notes.
            category (str): The category to filter the notes by.
            sorting (str): The sorting option for the notes.
            It should be one of the following: "newest", "oldest", "atoz", "ztoa".

        Returns:
            list: A list of all the retrieved notes.
        """
        type_sorting = {
            "newest": "ORDER BY created_at DESC;",
            "oldest": "ORDER BY created_at ASC;",
            "atoz": "ORDER BY note_name ASC;",
            "ztoa": "ORDER BY note_name DESC;",
        }
        if sorting not in type_sorting:
            raise ValueError(
                "The argument must be ('newest', 'oldest', 'atoz', 'ztoa')"
            )

        db_connector = DatabaseConnector()
        connection = db_connector.connect("notes")
        try:
            with connection.cursor() as cursor:
                if category != "All notes":
                    select_all_rows = (
                            "SELECT * FROM `%s` WHERE user_id = %%s AND note_category = %%s" % table_name
                            + type_sorting[sorting]
                    )
                    cursor.execute(select_all_rows, (user_id, category))
                else:
                    select_all_rows = (
                            "SELECT * FROM `%s` WHERE user_id = %%s" % table_name + " " + type_sorting[sorting]
                    )
                    cursor.execute(select_all_rows, (user_id,))

                all_notes_list = []

                rows = cursor.fetchall()
                # print(rows)
                for row in rows:
                    all_notes_list.append(row)
                return all_notes_list
        finally:
            db_connector.close()

    @staticmethod
    def select_note(table_name: str, user_id, note_id: int):
        """
        Retrieves a specific note from the specified table in the database.

        Args:
            table_name (str): The name of the table containing the note.
            note_id (int): The ID of the note to retrieve.

        Returns:
            dict: The information of the retrieved note.
        """
        db_connector = DatabaseConnector()
        connection = db_connector.connect("notes")
        try:
            with connection.cursor() as cursor:
                select_all_info = "SELECT * FROM `%s` WHERE user_id = %%s AND id = %%s" % table_name
                cursor.execute(select_all_info, (user_id, note_id))
                all_info_note = cursor.fetchall()
                return all_info_note
        finally:
            db_connector.close()

    @staticmethod
    def select_last_note(table_name: str):
        """
        Retrieves the ID of the last note in the specified table.

        Args:
            table_name (str): The name of the table.

        Returns:
            int: The ID of the last note.
        """
        db_connector = DatabaseConnector()
        connection = db_connector.connect("notes")
        try:
            with connection.cursor() as cursor:
                select_all_info = "SELECT * FROM `%s` " % table_name
                cursor.execute(select_all_info)
                all_notes_list = []

                rows = cursor.fetchall()

                for row in rows:
                    all_notes_list.append(row)

                return all_notes_list[-1]["id"]
        finally:
            db_connector.close()

    @staticmethod
    def select_number_characters(table_name: str, column_name: str):
        """
        Retrieves the maximum character length of a specific column in the specified table.

        Args:
            table_name (str): The name of the table containing the column.
            column_name (str): The name of the column to retrieve the character length for.

        Returns:
            int: The maximum character length of the specified column.
        """
        db_connector = DatabaseConnector()
        connection = db_connector.connect("notes")
        try:
            with connection.cursor() as cursor:
                select_all_info = (
                        "SELECT character_maximum_length "
                        "FROM information_schema.columns "
                        "WHERE table_name='%s' and column_name=%%s;" % table_name
                )
                cursor.execute(select_all_info, column_name)
                row = cursor.fetchall()
                return row[0]["CHARACTER_MAXIMUM_LENGTH"]
        finally:
            db_connector.close()
