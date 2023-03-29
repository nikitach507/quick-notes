from database.database_action import *


class NotesDatabaseAction:
    def __init__(self, head, description, additional, name_cat):
        self.head = head
        self.description = description
        self.additional = additional
        self.name_cat = name_cat

    def add_note(self, table_name):
        connection = connect_db()
        try:
            with connection.cursor() as cursor:
                insert_query = "INSERT INTO `%s` (head, description, additional, name_cat) " \
                               "VALUES (%%s, %%s, %%s, %%s);" % table_name
                cursor.execute(insert_query, (self.head, self.description, self.additional, self.name_cat))
                connection.commit()
                print("Adding a note was successful")
                print("#" * 20)
        finally:
            close_db(connection)

    def edit_note(self, table_name, note_id, new_head=None, new_desc=None, new_addit=None, new_cat=None):
        if new_head is None: new_head = self.head
        if new_desc is None: new_desc = self.description
        if new_addit is None: new_addit = self.additional
        if new_cat is None: new_cat = self.name_cat
        connection = connect_db()
        try:
            with connection.cursor() as cursor:
                update_query = "UPDATE `%s` SET " \
                               "head = %%s, description = %%s, additional = %%s, name_cat = %%s " \
                               "WHERE id = %%s;" % table_name
                cursor.execute(update_query, (new_head, new_desc, new_addit, new_cat, note_id))
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
    def select_all_notes(table_name, category):
        connection = connect_db()
        try:
            with connection.cursor() as cursor:
                if category == "All notes":
                    select_all_rows = "SELECT * FROM `%s`;" % table_name
                    cursor.execute(select_all_rows)
                else:
                    select_all_rows = "SELECT * FROM `%s` WHERE name_cat = %%s;" % table_name
                    cursor.execute(select_all_rows, category)
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
