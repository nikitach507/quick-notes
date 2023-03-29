from database.database_action import *


class CategoryDatabaseAction:
    def __init__(self, name_cat):
        self.name_cat = name_cat

    def add_category(self, table_name):
        connection = connect_db()
        try:
            with connection.cursor() as cursor:
                insert_query = "INSERT INTO `%s` (name_cat) " \
                               "VALUES (%%s);" % table_name
                cursor.execute(insert_query, self.name_cat)
                connection.commit()
                print("Adding a category was successful")
                print("#" * 20)
        finally:
            close_db(connection)

    @staticmethod
    def edit_category(table_name, name_cat_now, name_cat_after):
        connection = connect_db()
        try:
            with connection.cursor() as cursor:
                update_query = "UPDATE `%s` SET " \
                               "name_cat = %%s " \
                               "WHERE name_cat = %%s;" % table_name
                cursor.execute(update_query, (name_cat_after, name_cat_now))
                connection.commit()
            print("Editing the category was successful")
            print("#" * 20)
        finally:
            close_db(connection)

    @staticmethod
    def delete_category(table_name, name_cat_now):
        connection = connect_db()
        try:
            with connection.cursor() as cursor:
                delete_query = "DELETE FROM `%s` WHERE name_cat = %%s;" % table_name
                cursor.execute(delete_query, name_cat_now)
                connection.commit()
                print("Deleting the category was successful")
                print("#" * 20)
        finally:
            close_db(connection)

    @staticmethod
    def delete_all_categories(table_name):
        connection = connect_db()
        try:
            with connection.cursor() as cursor:
                delete_all_rows = "DELETE FROM `%s`;" % table_name
                cursor.execute(delete_all_rows)
                connection.commit()
                print("Deletion of all categories was successful")
                print("#" * 20)
        finally:
            close_db(connection)

    @staticmethod
    def select_all_categories(table_name):
        connection = connect_db()
        try:
            with connection.cursor() as cursor:
                select_all_rows = "SELECT name_cat FROM `%s`;" % table_name
                cursor.execute(select_all_rows)

                rows = cursor.fetchall()
                for row in rows:
                    print(row)
                print("#" * 20)
        finally:
            close_db(connection)

    @staticmethod
    def all_categories_list(table_name):
        connection = connect_db()
        try:
            with connection.cursor() as cursor:
                select_all_rows = "SELECT name_cat FROM `%s`;" % table_name
                cursor.execute(select_all_rows)

                rows = cursor.fetchall()
                all_cat_list = [row["name_cat"] for row in rows]
                return all_cat_list
        finally:
            close_db(connection)


# contact_data = CategoryAction("Movies")
# contact_data.all_categories_list("note_category")
