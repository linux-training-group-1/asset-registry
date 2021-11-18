import pymysql
import pymysql.cursors
import os

# Singleton connection
connection = None


# Connect to the database
def get_connection():
    global connection
    if connection is None:
        connection = pymysql.connect(host=os.environ['MYSQL_HOST'],
                                     user=os.environ['MYSQL_USER'],
                                     password=os.environ['MYSQL_PASSWORD'],
                                     database=os.environ['MYSQL_DB'],
                                     port=int(os.environ['MYSQL_PORT']),
                                     cursorclass=pymysql.cursors.DictCursor)
    return connection


def check_credentials(username, password, admin=True):
    conn = get_connection()
    # with connection:
    #     with connection.cursor() as cursor:
    #         # Create a new record
    #         sql = "INSERT INTO `users` (`email`, `password`) VALUES (%s, %s)"
    #         cursor.execute(sql, ('webmaster@python.org', 'very-secret'))
    #
    # # connection is not autocommit by default. So you must commit to save
    # # your changes.
    # connection.commit()

    with conn.cursor() as cursor:
        # Read a single record
        # TODO: check salt + hashed password
        sql = "SELECT `username` FROM `user` WHERE `admin`=%s and `username`=%s and `password`=%s"
        cursor.execute(sql, (admin, username, password))
        # Query should match only to one row if credentials are found
        return cursor.rowcount == 1