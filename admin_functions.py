sql_flush = "flush privileges;"
"""
Creates user at mysql level
Grants privileges at mysql level
Also deletes user at mysql level
"""


def create_User(my_db, db_name, my_cursor, username, password):
    try:
        sql_create_user = "CREATE USER '%s'@'localhost' IDENTIFIED BY '%s';" % (username, password)
        my_cursor.execute(sql_create_user)
        my_db.commit()
        sql_grant_user = "GRANT SELECT, ALTER, DELETE, INSERT, UPDATE on `%s`.* TO '%s'@'localhost';" % (
            db_name, username)
        my_cursor.execute(sql_grant_user)
        my_db.commit()
        my_cursor.execute(sql_flush)
        my_db.commit()
    except Exception as Ex:
        print("Error creating MySQL User: %s" % Ex)
    else:
        print("Already created")
    finally:
        return True


def del_user(my_db, my_cursor, del_username):
    sql_del_user = "DROP USER '%s'@'localhost';" % del_username
    my_cursor.execute(sql_del_user)
    my_db.commit()
    my_cursor.execute(sql_flush)
    my_db.commit()
    print("successfully deleted user")
