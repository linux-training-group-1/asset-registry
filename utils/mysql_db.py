import os

import pymysql
import pymysql.cursors

# Singleton connection
_connection = None


# Connect to the database
def _get_connection():
    global _connection
    if _connection is None:
        _connection = pymysql.connect(host=os.environ['MYSQL_HOST'],
                                      user=os.environ['MYSQL_USER'],
                                      password=os.environ['MYSQL_PASSWORD'],
                                      database=os.environ['MYSQL_DB'],
                                      port=int(os.environ['MYSQL_PORT']),
                                      cursorclass=pymysql.cursors.DictCursor)
    return _connection


def check_credentials(username, password, admin=True):
    conn = _get_connection()
    with conn.cursor() as cursor:
        # Read a single record
        # TODO: check salt + hashed password
        sql = "SELECT `username` FROM `user` WHERE `admin`=%s and `username`=%s and `password`=%s"
        cursor.execute(sql, (admin, username, password))
        # Query should match only to one row if credentials are found
        return cursor.rowcount == 1


def get_item_by_id(id):
    conn = _get_connection()
    with conn.cursor() as cursor:
        # Read a single record
        sql = "SELECT * FROM `asset` WHERE `id`=%s"
        cursor.execute(sql, id)
        # Query should match only to one row if credentials are found
        return cursor.fetchone()


def get_items_by_name(name, limit):
    conn = _get_connection()
    with conn.cursor() as cursor:
        # Read a single record
        sql = "SELECT * FROM `asset` WHERE MATCH(`name`) AGAINST(%s IN NATURAL LANGUAGE MODE) limit %s"
        cursor.execute(sql, name, limit)
        # Query should match multiple rows
        return cursor.fetchall()


def add_item(name, owner, description, location, criticality):
    conn = _get_connection()
    with conn.cursor() as cursor:
        sql = "INSERT INTO `asset` (`name`, `owner`,`description`,`location`,`criticality`) VALUES (%s, %s, %s, %s, %s)"
        cursor.execute(sql, (name, owner, description, location, criticality))
    conn.commit()
