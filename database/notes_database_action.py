from typing import Literal

from database.database_action import *


class NotesDatabaseAction:
    def __init__(self, note_name, note_description, note_category):
        self.note_name = note_name
        self.note_description = note_description
        self.note_category = note_category

    def add_note(self, table_name):
        connection = connect_db()
        try:
            with connection.cursor() as cursor:
                insert_query = "INSERT INTO `%s` (note_name, note_description, note_category) " \
                               "VALUES (%%s, %%s, %%s);" % table_name
                cursor.execute(insert_query, (self.note_name, self.note_description, self.note_category))
                connection.commit()
                print("Adding a note was successful")
                print("#" * 20)
        finally:
            close_db(connection)

    def edit_note(self, table_name, note_id, new_name=None, new_desc=None, new_category=None):
        if new_name is None: new_name = self.note_name
        if new_desc is None: new_desc = self.note_description
        if new_category is None: new_category = self.note_category
        connection = connect_db()
        try:
            with connection.cursor() as cursor:
                update_query = "UPDATE `%s` SET " \
                               "note_name = %%s, note_description = %%s, note_category = %%s " \
                               "WHERE id = %%s;" % table_name
                cursor.execute(update_query, (new_name, new_desc, new_category, note_id))
                connection.commit()
            print("Editing the note was successful")
            print("#" * 20)
        finally:
            close_db(connection)

    @staticmethod
    def delete_note(table_name, note_id):
        connection = connect_db()
        try:
            with connection.cursor() as cursor:
                delete_query = "DELETE FROM `%s` WHERE id = %%s;" % table_name
                cursor.execute(delete_query, note_id)
                connection.commit()
                print("Deleting the note was successful")
                print("#" * 20)
        finally:
            close_db(connection)

    @staticmethod
    def delete_all_notes(table_name):
        connection = connect_db()
        try:
            with connection.cursor() as cursor:
                delete_all_rows = "DELETE FROM `%s`;" % table_name
                cursor.execute(delete_all_rows)
                connection.commit()
                print("Deletion of all notes was successful")
                print("#" * 20)
        finally:
            close_db(connection)

    @staticmethod
    def select_all_notes(table_name, category, sorting: Literal["newest", "oldest", "atoz", "ztoa"]):
        """
            This function writes out data with sorting.

            :param table_name: Name of the required table.
            :type table_name: str
            :param category: Name of the notes' category.
            :type category: str
            :param sorting: The way to sort notes.
            :type sorting: str
            """
        type_sorting = {"newest": "ORDER BY created_at DESC;",
                        "oldest": "ORDER BY created_at ASC;",
                        "atoz": "ORDER BY note_name ASC;",
                        "ztoa": "ORDER BY note_name DESC;"
                        }
        if sorting not in type_sorting:
            raise ValueError("Аргумент должен быть ('newest', 'oldest', 'atoz', 'ztoa')")

        connection = connect_db()
        try:
            with connection.cursor() as cursor:

                if category != "All notes":
                    select_all_rows = "SELECT * FROM `%s` WHERE note_category = %%s" % table_name + type_sorting[sorting]
                    cursor.execute(select_all_rows, category)
                else:
                    select_all_rows = "SELECT * FROM `%s` " % table_name + type_sorting[sorting]
                    cursor.execute(select_all_rows)

                all_notes_dict = list()
                rows = cursor.fetchall()
                for row in rows:
                    all_notes_dict.append(row)
                return all_notes_dict
        finally:
            close_db(connection)

    @staticmethod
    def select_number_characters(table_name, column_name):
        connection = connect_db()
        try:
            with connection.cursor() as cursor:
                select_all_info = "SELECT character_maximum_length " \
                                  "FROM information_schema.columns " \
                                  "WHERE table_name='%s' and column_name=%%s;" % table_name
                cursor.execute(select_all_info, column_name)
                row = cursor.fetchall()
                return row[0]["CHARACTER_MAXIMUM_LENGTH"]
        finally:
            close_db(connection)

# contact_data = NotesAction("Dune", "Description about Dune", "Additional about Dune", "Books")
# print(contact_data.delete_note(table_name="notes_info", note_id=12))
