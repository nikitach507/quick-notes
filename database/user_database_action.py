from database.connect_database import DatabaseConnector


class UserDatabaseAction:
    @staticmethod
    def add_user_info(table_name, email, password_hash, salt, first_name,
                      last_name):
        db_connector = DatabaseConnector()
        connection = db_connector.connect("userauth")
        try:
            with connection.cursor() as cursor:
                add_user = "INSERT INTO `%s` (email, password_hash, " \
                                  "salt, first_name, last_name, authenticated) " \
                                  "VALUES (%%s, %%s, %%s, %%s, %%s, %%s);" % table_name
                cursor.execute(add_user, (email, password_hash, salt, first_name, last_name, False))
                connection.commit()
                print("Adding a user was successful")
                print("#" * 20)
        finally:
            db_connector.close()

    @staticmethod
    def output_all_data_in_column(table_name, column_name):
        db_connector = DatabaseConnector()
        connection = db_connector.connect("userauth")
        try:
            with connection.cursor() as cursor:
                select_data = "SELECT %s FROM %s" % (column_name, table_name)
                cursor.execute(select_data)

                rows = cursor.fetchall()
                all_data_in_column = [row[column_name] for row in rows]
                return all_data_in_column
        finally:
            db_connector.close()

    @staticmethod
    def output_user_hash_psw_salt(table_name, email):
        db_connector = DatabaseConnector()
        connection = db_connector.connect("userauth")
        try:
            with connection.cursor() as cursor:
                select_data = "SELECT password_hash, salt FROM `%s` WHERE email=%%s" % table_name
                cursor.execute(select_data, (email,))

                rows = cursor.fetchall()
                for row in rows:
                    return row
        finally:
            db_connector.close()

    @staticmethod
    def active_user_id(table_name, email):
        db_connector = DatabaseConnector()
        connection = db_connector.connect("userauth")
        try:
            with connection.cursor() as cursor:
                update_auth_user = "UPDATE %s SET authenticated = TRUE WHERE email = %%s;" % table_name
                cursor.execute(update_auth_user, (email,))
                connection.commit()
                print("User email is active")
                print("#" * 20)
                select_data = "SELECT id FROM `%s` WHERE email=%%s" % table_name
                cursor.execute(select_data, (email,))

                rows = cursor.fetchall()
                return rows[0]["id"]
        finally:
            db_connector.close()
