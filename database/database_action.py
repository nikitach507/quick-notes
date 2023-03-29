import pymysql.cursors
from database.config import *


def connect_db():
    try:
        connect_to_database = pymysql.connect(
            host=hostname,
            port=3306,
            user=username,
            password=password,
            database=database,
            cursorclass=pymysql.cursors.DictCursor
        )
        return connect_to_database
    except Exception as ex:
        print("Failed connection with database")
        print(ex)


# def create_table(connect_to_database):
#     try:
#         with connect_to_database.cursor() as cursor:
#             create_table_query = "CREATE TABLE `note_category` (name_cat varchar(32));"
#             cursor.execute(create_table_query)
#             print("Table created")
#     finally:
#         close_db(connect_to_database)
#
#
# def edit_table(connect_to_database):
#     try:
#         with connect_to_database.cursor() as cursor:
#             create_table_query = "ALTER TABLE `notes_info` ADD name_cat VARCHAR (32);"
#             cursor.execute(create_table_query)
#             print("Table created")
#     finally:
#         close_db(connect_to_database)


def close_db(connect_to_database):
    if connect_to_database:
        connect_to_database.close()
