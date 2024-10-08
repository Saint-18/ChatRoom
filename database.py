import mysql.connector
import dotenv

""" 
This file controls interaction with the MySQL database
for more information on the mysql.connector package
see documentation at 
https://dev.mysql.com/doc/connector-python/en/connector-python-examples.html
"""


def create_database_connection():
    """
    Creates a connection to the MySQL database
    Inputs: None
    Return: cnx - MySQLConnection object
    """
    # Read database credentials from .env file
    credentials = dotenv.dotenv_values(".env")

    # database configuration information
    config = {
        "user": credentials.get("DATABASE_USER"),
        "password": credentials.get("DATABASE_PW"),
        "host": "127.0.0.1",
        "database": "chatapp",
        "raise_on_warnings": True,
    }

    # establish a connection to the database
    cnx = mysql.connector.connect(**config)
    # Return the connection object
    return cnx


def get_messages(cnx: object, chat_id: int):
    """
    Retrieves all message for the requested chatroom
    Input: cnx - MySQL database connection object, chat_id - chatroom identifier
    Returns: Array of JSON objects
    """
    # Create a cursor from the connection object (cnx)
    # dictionary=True returns results as JSON
    cursor = cnx.cursor(dictionary=True)

    # Create the database query
    query = (
        "SELECT Users.username, Messages.message_body, Messages.created_at, Messages.message_id "
        "FROM Messages JOIN Users ON Messages.user_id = Users.user_id JOIN Chats ON Messages.chat_id = Chats.chat_id "
        "WHERE Messages.status = 'approved' AND Chats.chat_id = %s "
        "ORDER BY Messages.created_at;"
    )

    # Execute the query
    cursor.execute(query, (chat_id,))
    # Fetch results
    results = cursor.fetchall()

    return results


def create_message(cnx: object, chat_id: int, username: str, message_body: str):
    """
    Posts a new message to the requested chatroom
    Input: cnx - MySQL database connection object, chat_id - chatroom identifier
           username - logged in user, message_body - text to post
    Returns: Boolean
    """
    try:
        # Create a cursor from the connection object (cnx)
        cursor = cnx.cursor()

        # Create the database query
        query = (
            "INSERT INTO Messages (chat_id, user_id, message_body, status) "
            "VALUES (%s, "
            "(SELECT user_id FROM Users WHERE username = %s), "
            "%s, 'approved');"
        )

        # Execute the query
        cursor.execute(query, (chat_id, username, message_body))
        cnx.commit()
        return True
    except:
        return False


def validate_user(cnx: object, username: str, password: str):
    """
    Validates username and password, returns True if approved for login
    Input: cnx - MySQL database connection object, username - string username, password - string password
    Returns: Array of JSON objects
    """
    # Create a cursor from the connection object (cnx)
    cursor = cnx.cursor()

    # Create the database query
    query = (
        # Looking for user_id matching supplied credentials
        "SELECT Users.user_id "
        "FROM Users "
        "WHERE Users.username = %s AND Users.password_hash = %s;"
    )

    # Execute the query
    cursor.execute(query, (username, password))
    # Fetch results
    user_id = cursor.fetchall()
    if user_id:
        return True
    else:
        return False


def get_approved_chats(cnx: object, username: str):
    """
    Gets a list of approved chats and role within chat
    Input: cnx - MySQL database connection object, username - string username
    Returns: Array of JSON objects
    """

    # Create a cursor from the connection object (cnx)
    # dictionary=True returns results as JSON
    cursor = cnx.cursor(dictionary=True)

    # Create the database query
    query = (
        "SELECT Chats.chat_id, Chats.chat_title, Chat_Members.role "
        "FROM Chats JOIN Chat_Members ON Chats.chat_id = Chat_Members.chat_id JOIN Users ON Users.user_id = Chat_Members.user_id "
        "WHERE Users.username = %s;"
    )

    # Execute the query
    cursor.execute(query, (username,))
    # Fetch results
    results = cursor.fetchall()

    return results


def delete_message(cnx, message_id):
    """
    Hides specified message
    Input: cnx - MySQL database connection object, message_id - identifier for message
    Returns: Boolean
    """
    try:
        # Create a cursor from the connection object (cnx)
        cursor = cnx.cursor()

        # Create the database query
        query = "UPDATE Messages SET status = 'hidden' WHERE message_id = %s;"

        # Execute the query
        cursor.execute(query, (message_id,))
        cnx.commit()
        return True
    except:
        return False


def close_database_connection(cnx: object):
    """
    Closes the connection to the database
    Input: cnx - MySQLConnection object
    Return: None
    """
    if cnx.is_connected():
        cnx.close()
